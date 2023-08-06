#! /usr/bin/env python

import json
import logging
import os
import shutil
from hashlib import sha1
from pathlib import Path
from string import ascii_letters, digits
from subprocess import run
from tempfile import TemporaryDirectory

import boto3

HERE = Path(__file__).parent
fmt = "%(levelname)s:%(asctime).19s: %(message)s"
logging.basicConfig(format=fmt)
logger = logging.getLogger("ozark")
lambda_client = boto3.client("lambda")
event_client = boto3.client("events")
log_client = boto3.client("logs")


def create_event_rule(
    function_arn,
    function_name,
    expression,
    state="ENABLED",
    event_input=None,
):

    # Rule name is the expression itself
    keep = ascii_letters + digits
    rule_name = "".join(l for l in expression if l in keep)

    rule_id = f"{function_name}_{rule_name}"
    # Put an event rule
    logger.info('Create or update rule "%s"', rule_id)
    rule_resp = event_client.put_rule(
        Name=rule_id,
        ScheduleExpression=expression,
        State=state,
    )

    # Add new target
    target_input = json.dumps(event_input or {})
    digest = sha1(target_input.encode()).hexdigest()
    # if function name gest too long, hash collision may become an issue
    assert len(function_name) < 50, "Function name too long"
    target_id = f"{function_name}_{digest}"[:64]
    logger.info('Create or update target "%s"', target_id)
    event_client.put_targets(
        Rule=rule_id,
        Targets=[
            {
                "Id": target_id,
                "Arn": function_arn,
                "Input": target_input,
            }
        ],
    )

    # Remove existing permissions
    try:
        lambda_client.remove_permission(
            FunctionName=function_name,
            StatementId=f"{rule_name}_perm",
        )
    except lambda_client.exceptions.ResourceNotFoundException:
        pass

    # Add permission
    lambda_client.add_permission(
        FunctionName=function_name,
        StatementId=f"{rule_name}_perm",
        Action="lambda:InvokeFunction",
        Principal="events.amazonaws.com",
        SourceArn=rule_resp["RuleArn"],
    )


def list_rule(lambda_name):
    # Find lambda arn
    lambda_arn = None
    for name, arn in list_lambda(lambda_name):
        if name == lambda_name:
            lambda_arn = arn
            break
    else:
        return

    # Get rules
    kw = {"TargetArn": lambda_arn}
    while True:
        resp = event_client.list_rule_names_by_target(**kw)
        for name in resp["RuleNames"]:
            yield name
        # Paginate
        token = resp.get("NextToken")
        if not token:
            return
        kw["NextToken"] = token


def list_rule_targets(rule_name):
    # Get targets
    kw = {"Rule": rule_name}
    while True:
        resp = event_client.list_targets_by_rule(**kw)
        for target in resp["Targets"]:
            yield target["Id"]
        # Paginate
        token = resp.get("NextToken")
        if not token:
            return
        kw["NextToken"] = token


def delete_rule(name):
    # Find associated targets
    logger.info('Delete rule "%s"', name)
    target_ids = list(list_rule_targets(name))
    event_client.remove_targets(Rule=name, Ids=target_ids)
    event_client.delete_rule(Name=name)


def create_layer_zip(req_file):
    zip_file = Path("layer.zip")
    logger.info("create artifact (in %s)", zip_file)
    with TemporaryDirectory() as tdir:
        module_dir = Path(tdir) / "python"
        os.mkdir(module_dir)
        args = ["pip", "install", "-t", module_dir, "-r", req_file]
        run(args)
        # Zip folder
        shutil.make_archive("layer", "zip", tdir)

    # Read content and remove file
    content = zip_file.open("rb").read()
    zip_file.unlink()
    return content


def list_layer(prefix=None):
    kw = {}
    while True:
        resp = lambda_client.list_layers(**kw)
        for lyr in resp["Layers"]:
            name = lyr["LayerName"]
            if prefix and not name.startswith(prefix):
                continue
            arn = lyr["LatestMatchingVersion"]["LayerVersionArn"]
            yield name, arn
        # Paginate
        marker = resp.get("NextMarker")
        if not marker:
            return
        kw = {"Marker": marker}


def delete_layer(name):
    try:
        resp = lambda_client.list_layer_versions(LayerName=name)
    except lambda_client.exceptions.ResourceNotFoundException:
        logger.info("No layer '%s' found" % name)
    else:
        versions = resp.get("LayerVersions", [])
        for version in versions:
            logger.debug("Delete layer version %s " % version["Version"])
            lambda_client.delete_layer_version(
                LayerName=name,
                VersionNumber=version["Version"],
            )
        logger.info("Layer %s deleted" % name)


def publish_layer(name, req_file, desc=None):
    # Create zip
    zipped_code = create_layer_zip(req_file)
    resp = lambda_client.publish_layer_version(
        LayerName=name,
        Description=desc or name,
        Content={"ZipFile": zipped_code},
        CompatibleRuntimes=["python3.7"],
        LicenseInfo="",
    )
    layer_arn = resp["LayerVersionArn"]
    logger.debug("New layer ARN: %s", layer_arn)
    return layer_arn


def list_lambda(prefix):
    kw = {}
    while True:
        resp = lambda_client.list_functions(**kw)
        for lmbd in resp["Functions"]:
            name = lmbd["FunctionName"]
            if prefix and not name.startswith(prefix):
                continue
            yield name, lmbd["FunctionArn"]
        # Paginate
        marker = resp.get("NextMarker")
        if not marker:
            return
        kw = {"Marker": marker}


def delete_lambda(name):
    # Delete associated rules
    for rule_name in list_rule(name):
        delete_rule(rule_name)

    try:
        lambda_client.delete_function(
            FunctionName=name,
        )
        logger.info("Function %s deleted" % name)
    except lambda_client.exceptions.ResourceNotFoundException:
        logger.info("No existing lambda to delete")
        pass


def create_lambda(name, files, role_arn=None, layers=None, env=None):
    # Inject handler
    files.append(HERE / "ozark_handler.py")

    # Create zip
    # TODO handle non-top-level files (as such)
    with TemporaryDirectory() as tdir:
        for filename in files:
            shutil.copy(filename, tdir)
        shutil.make_archive(name, "zip", tdir)
    zip_file = Path(f"{name}.zip")
    zipped_code = zip_file.open("rb").read()
    zip_file.unlink()

    kw = {
        "FunctionName": name,
        "Runtime": "python3.7",
        "Role": role_arn,
        "Handler": "ozark_handler.lambda_handler",
        "Timeout": 600,
        "Environment": dict(Variables=env or {}),
        "Layers": layers or [],
    }

    # Update function if it already exists
    try:
        fn = lambda_client.get_function(FunctionName=name)
    except lambda_client.exceptions.ResourceNotFoundException:
        fn = None

    if fn is not None:
        logger.info('Update function "%s"' % name)
        lambda_client.update_function_code(
            FunctionName=name,
            ZipFile=zipped_code,
        )
        resp = lambda_client.update_function_configuration(**kw)

    else:
        logger.info('Create function "%s"' % name)
        kw["Code"] = dict(ZipFile=zipped_code)
        resp = lambda_client.create_function(**kw)

    arn = resp["FunctionArn"]
    logger.info("Lambda create (arn: %s)", arn)


def invoke_lambda(name, payload):
    resp = lambda_client.invoke(
        FunctionName=name,
        InvocationType="RequestResponse",  # Event
        Payload=json.dumps(payload),
    )
    # Read and decode payload
    resp["Payload"] = json.loads(resp["Payload"].read())
    return resp


def get_logs(lambda_name):
    log_group_name = f"/aws/lambda/{lambda_name}"
    stream_resp = log_client.describe_log_streams(logGroupName=log_group_name)
    log_streams = stream_resp["logStreams"]
    log_streams.sort(key=lambda x: x["firstEventTimestamp"])
    for log_stream in log_streams:
        log_resp = log_client.get_log_events(
            logGroupName=log_group_name, logStreamName=log_stream["logStreamName"]
        )

        events = log_resp["events"]
        events.sort(key=lambda x: x["timestamp"])
        for event in events:
            yield event["timestamp"], event["message"]

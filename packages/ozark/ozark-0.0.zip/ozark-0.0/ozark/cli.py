import argparse
import importlib
import os
from datetime import datetime
from pathlib import Path
from pprint import pprint

from omegaconf import OmegaConf

from . import __version__
from .utils import (
    create_event_rule,
    create_lambda,
    delete_lambda,
    delete_layer,
    get_logs,
    invoke_lambda,
    list_lambda,
    list_layer,
    logger,
    publish_layer,
)

# The `inc` resolver allows to include/inject values from another
# file. Useful to compose different files bases on deployment target
# or to include secrets from a non-versionned file.
OmegaConf.register_resolver("inc", OmegaConf.load)


def run(args):
    cfg = OmegaConf.from_dotlist(args.icfg)
    if args.config:
        cfg = OmegaConf.merge(OmegaConf.load(args.config), cfg)
    cfg = OmegaConf.to_container(cfg)

    file_path, fn = args.fn.rsplit(".", 1)
    p = Path(".")
    for part in file_path.split("."):
        p = p / part

    env = OmegaConf.to_container(OmegaConf.load(args.env)) if args.env else {}

    spec = importlib.util.spec_from_file_location(part, f"{p}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Replace env & run code
    os.environ.update(env)
    res = getattr(module, fn)(cfg)
    if res is not None:
        pprint(res)


def lambda_(args):
    layer_arns = []
    for name in args.layer:
        for match_name, arn in list_layer(name):
            if match_name == name:
                layer_arns.append(arn)
                break
        else:
            exit(f'Layer "{name}" not found')

    env = OmegaConf.to_container(OmegaConf.load(args.env)) if args.env else None

    create_lambda(
        args.name, args.files, role_arn=args.role_arn, layers=layer_arns, env=env
    )


def layer(args):
    arn = publish_layer(args.name, args.file, args.desc)
    print(arn)


def del_lambda(args):
    for name in args.names:
        delete_lambda(name)


def del_layer(args):
    for name in args.names:
        delete_layer(name)


def invoke(args):
    cfg = OmegaConf.from_dotlist(args.icfg)
    if args.config:
        cfg = OmegaConf.merge(OmegaConf.load(args.config), cfg)
    cfg = OmegaConf.to_container(cfg)

    resp = invoke_lambda(
        args.name,
        {
            "fn": args.fn,
            "cfg": cfg,
        },
    )
    if args.full:
        pprint(resp)
    else:
        payload = resp["Payload"]
        if payload is not None:
            pprint(payload)


def list_lyr(args):
    for name, arn in list_layer(args.prefix):
        print(name, "\t", arn)


def list_lmbd(args):
    for name, arn in list_lambda(args.prefix):
        print(name, "\t", arn)


def schedule(args):
    lambda_arn = None
    for name, arn in list_lambda(args.name):
        if name == args.name:
            lambda_arn = arn
        break
    else:
        exit(f'Lambda "{args.name}" not found')
    expression = f"rate({args.rate})"
    cfg = OmegaConf.from_dotlist(args.icfg)
    if args.config:
        cfg = OmegaConf.merge(OmegaConf.load(args.config), cfg)

    cfg = OmegaConf.to_container(cfg)
    event_input = {
        "fn": args.fn,
        "cfg": cfg,
    }
    create_event_rule(lambda_arn, args.name, expression, event_input=event_input)


def log(args):
    for ts, event in get_logs(args.name):
        ts = datetime.fromtimestamp(ts / 1000).isoformat()
        for line in event.splitlines():
            print(ts, "\t", line)


def main():
    parser = argparse.ArgumentParser(
        prog="ozark",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-v", "--verbose", action="count", default=0, help="Increase verbosity"
    )

    subparsers = parser.add_subparsers(dest="command")

    # version
    parser_version = subparsers.add_parser("version", description="Print version")
    parser_version.set_defaults(func=lambda a: print(__version__))

    # lambda
    parser_lambda = subparsers.add_parser("lambda", description="Deploy Lambda")
    parser_lambda.add_argument("files", nargs="+", help="Upload files")
    parser_lambda.add_argument("-n", "--name", help="Lambda Name")
    parser_lambda.add_argument("-a", "--role-arn", help="Lambda role arn")
    parser_lambda.add_argument(
        "-e", "--env", help="Load environment variables from given file"
    )
    parser_lambda.add_argument("-l", "--layer", nargs="*", help="Layer names")
    parser_lambda.set_defaults(func=lambda_)

    # layer
    parser_layer = subparsers.add_parser(
        "layer", description="Create layer from requirement file"
    )
    parser_layer.add_argument("name", help="Layer name")
    parser_layer.add_argument("file", help="Requirements file")
    parser_layer.add_argument("-d", "--desc", help="Description")
    parser_layer.set_defaults(func=layer)

    # run
    parser_run = subparsers.add_parser("run", description="Run script locally")
    parser_run.add_argument(
        "fn", action="store", help="Function to run (example: my_script.my_function"
    )
    parser_run.add_argument(
        "icfg", nargs="*", help="Inline Config (example: verbose=true host.port=80)"
    )
    parser_run.add_argument("-c", "--config", help="From yaml file")
    parser_run.add_argument(
        "-e", "--env", help="Load environment variables from given file"
    )
    parser_run.set_defaults(func=run)

    # invoke
    parser_invoke = subparsers.add_parser("invoke", description="Invoke Lambda")
    parser_invoke.add_argument("name", help="Lambda name")
    parser_invoke.add_argument("fn", help="Function to call")
    parser_invoke.add_argument(
        "icfg", nargs="*", help="Inline Config (example: verbose=true host.port=80)"
    )
    parser_invoke.add_argument(
        "-f", "--full", action="store_true", help="Print invocation ouput"
    )
    parser_invoke.add_argument("-c", "--config", help="From yaml file")
    parser_invoke.set_defaults(func=invoke)

    # delete lambda
    parser_del_lambda = subparsers.add_parser(
        "delete-lambda", description="Delete Lambda"
    )
    parser_del_lambda.add_argument("names", nargs="*", help="Lambda names")
    parser_del_lambda.set_defaults(func=del_lambda)

    # delete layer
    parser_del_layer = subparsers.add_parser("delete-layer", description="Delete layer")
    parser_del_layer.add_argument("names", nargs="*", help="Layer names")
    parser_del_layer.set_defaults(func=del_layer)

    # list lambda
    parser_list_lambda = subparsers.add_parser("list-lambda", description="List Lambda")
    parser_list_lambda.add_argument("-p", "--prefix", help="Filter on prefix")
    parser_list_lambda.set_defaults(func=list_lmbd)

    # list layer
    parser_list_layer = subparsers.add_parser("list-layer", description="List Layer")
    parser_list_layer.add_argument("-p", "--prefix", help="Filter on prefix")
    parser_list_layer.set_defaults(func=list_lyr)

    # schedule lambda
    parser_schedule = subparsers.add_parser("schedule", description="Schedule Lambda")
    parser_schedule.add_argument("name", help="Lambda name")
    parser_schedule.add_argument("rate", help="Rate. Example: '5 minutes'")
    parser_schedule.add_argument("fn", help="Functio to call")
    parser_schedule.add_argument(
        "icfg", nargs="*", help="Inline Config (example: verbose=true host.port=80)"
    )
    parser_schedule.add_argument("-c", "--config", help="From yaml file")
    parser_schedule.set_defaults(func=schedule)

    # get lambda logs
    parser_log = subparsers.add_parser("log", description="Get lambda logs")
    parser_log.add_argument("name", help="Lambda name")
    parser_log.set_defaults(func=log)

    args = parser.parse_args()
    if args.verbose == 1:
        logger.setLevel("INFO")
    elif args.verbose > 1:
        logger.setLevel("DEBUG")

    if not args.command:
        parser.print_help()
        return
    args.func(args)

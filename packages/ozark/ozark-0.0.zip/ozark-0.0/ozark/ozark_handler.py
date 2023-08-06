from pathlib import Path
import importlib


def lambda_handler(event, context):
    fn = event['fn']
    cfg = event['cfg']
    file_path, fn = fn.rsplit('.', 1)
    p = Path('.')
    for part in file_path.split('.'):
        p = p / part

    spec = importlib.util.spec_from_file_location(part, f'{p}.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    res = getattr(module, fn)(cfg)
    return res

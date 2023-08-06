# Quickstart

First create a simple script `hello_world.py`:

```python
def run(cfg):
    name = cfg['name']
    return f'hello {name} between {cfg["from_time"]} and {cfg["to_time"]}'
```

You can then run it locally:

```
$ ozark run hello_world.run name=world from_time=2020-01-01 to_time=2020-01-02
'hello world between 2020-01-01 and 2020-01-02'
```

Deploy it:

```
$ ozark lambda hello_world.py  -n LAMBDA_NAME -a ROLE_ARN
```

And invoke it:

```
$ ozark invoke LAMBDA_NAME hello_world.run name=spam from_time=2020-01-01 to_time=2020-01-02
hello spam between 2020-01-01 and 2020-01-02
```

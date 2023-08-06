# MeterSphere2Case

Convert MeterSphere data to yaml testcases for HttpRunner.

[Click here](https://github.com/metersphere/chrome-extensions)  download the chrome plugin 

## usage

To see ``MeterSphere2Case`` version:

```shell
$ python main.py -V
0.0.1
```

To see available options, run

```shell
$ python main.py -h
usage: main.py [-h] [-V] [--log-level LOG_LEVEL]
               [MeterSphere_testset_file] [output_testset_file]

Convert MeterSphere testcases to JSON testcases for HttpRunner.

positional arguments:
  MeterSphere_testset_file  Specify MeterSphere testset file.
  output_testset_file   Optional. Specify converted JSON testset file.

optional arguments:
  -h, --help            show this help message and exit
  -V, --version         show version
  --log-level LOG_LEVEL
                        Specify logging level, default is INFO.
```

## examples

In most cases, you can run ``MeterSphere2Case`` like this:

```shell
$ python3 main.py test/test.json output.json
INFO:root:Generate JSON testset successfully: output.json
```

As you see, the first parameter is MeterSphere source file path, and the second is converted JSON file path.

The output testset file type is detemined by the suffix of your specified file.

If you only specify MeterSphere source file path, the output testset is in JSON format by default and located in the same folder with source file.

```shell
$ python3 main.py test/test.json
INFO:root:Generate JSON testset successfully: test/test.output.json
```

## generated testset

generated JSON testset ``output.json`` shows like this:

```json
[
    {
        "test": {
            "name": "/api/v1/Account/Login",
            "request": {
                "method": "POST",
                "url": "https://httprunner.top/api/v1/Account/Login",
                "headers": {
                    "Content-Type": "application/json"
                },
                "json": {
                    "UserName": "test001",
                    "Pwd": "123",
                    "VerCode": ""
                }
            },
            "validate": []
        }
    }
]
```


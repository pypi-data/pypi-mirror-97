# lintaosp

[![Actions Status](https://github.com/craftslab/lintaosp/workflows/CI/badge.svg?branch=master&event=push)](https://github.com/craftslab/lintaosp/actions?query=workflow%3ACI)
[![Docker](https://img.shields.io/docker/pulls/craftslab/lintaosp)](https://hub.docker.com/r/craftslab/lintaosp)
[![License](https://img.shields.io/github/license/craftslab/lintaosp.svg?color=brightgreen)](https://github.com/craftslab/lintaosp/blob/master/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/lintaosp.svg?color=brightgreen)](https://pypi.org/project/lintaosp)
[![Tag](https://img.shields.io/github/tag/craftslab/lintaosp.svg?color=brightgreen)](https://github.com/craftslab/lintaosp/tags)



## Introduction

*lintaosp* is a lint worker of *[lintflow](https://github.com/craftslab/lintflow/)* on AOSP written in Python.



## Prerequisites

- Android lint >= 4.1.0
- gRPC >= 1.36.0
- Python >= 3.7.0



## Run

- **Local mode**

```bash
git clone https://github.com/craftslab/lintaosp.git

cd lintaosp
pip install -Ur requirements.txt
python aosp.py --config-file="config.yml" --lint-project="project" --output-file="output.json"
```



- **Service mode**

```bash
git clone https://github.com/craftslab/lintaosp.git

cd lintaosp
pip install -Ur requirements.txt
python aosp.py --config-file="config.yml" --listen-url="127.0.0.1:9090"
```



## Docker

- **Local mode**

```bash
git clone https://github.com/craftslab/lintaosp.git

cd lintaosp
docker build --no-cache -f Dockerfile -t craftslab/lintaosp:latest .
docker run -it -v /tmp:/tmp craftslab/lintaosp:latest ./lintaosp --config-file="config.yml" --lint-project="/tmp/project" --output-file="/tmp/output.json"
```



- **Service mode**

```bash
git clone https://github.com/craftslab/lintaosp.git

cd lintaosp
docker build --no-cache -f Dockerfile -t craftslab/lintaosp:latest .
docker run -it -p 9090:9090 craftslab/lintaosp:latest ./lintaosp --config-file="config.yml" --listen-url="127.0.0.1:9090"
```



## Usage

```
usage: aosp.py [-h] --config-file CONFIG_FILE
               [--lint-project LINT_PROJECT | --listen-url LISTEN_URL]
               [--output-file OUTPUT_FILE] [-v]

Lint AOSP

optional arguments:
  -h, --help            show this help message and exit
  --config-file CONFIG_FILE
                        config file (.yml)
  --lint-project LINT_PROJECT
                        lint project (/path/to/project)
  --listen-url LISTEN_URL
                        listen url (host:port)
  --output-file OUTPUT_FILE
                        output file (.json|.txt|.xlsx)
  -v, --version         show program's version number and exit
```



## Settings

*lintaosp* parameters can be set in the directory [config](https://github.com/craftslab/lintaosp/blob/master/lintaosp/config).

An example of configuration in [config.yml](https://github.com/craftslab/lintaosp/blob/master/lintaosp/config/config.yml):

```yaml
apiVersion: v1
kind: worker
metadata:
  name: lintaosp
spec:
  sdk:
    - Correctness
    - Correctness:Messages
    - Security
    - Compliance
    - Performance
    - Performance:Application Size
    - Usability:Typography
    - Usability:Icons
    - Usability
    - Productivity
    - Accessibility
    - Internationalization
    - Internationalization:Bidirectional Text
```



## Design

![design](design.png)



## Errorformat

- **Error type**

```
E: Error
I: Information
W: Warning
```

- **JSON format**

```json
{
  "lintaosp": [
    {
      "file": "name",
      "line": 1,
      "type": "Error",
      "details": "text"
    }
  ]
}
```

- **Text format**

```text
lintaosp:{file}:{line}:{type}:{details}
```



## License

Project License can be found [here](LICENSE).



## Reference

- [Android lint](https://developer.android.com/studio/write/lint)
- [errorformat](https://github.com/reviewdog/errorformat)
- [gRPC](https://grpc.io/docs/languages/python/)
- [protocol-buffers](https://developers.google.com/protocol-buffers/docs/proto3)
- [reviewdog](https://github.com/reviewdog/reviewdog)

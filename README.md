## AWS Credentials manager


### Building

```shell
uv build
```

### Installing


```shell
python -m pip install dist/aws_credentials_manager-0.2.1-py3-none-any.whl
```

Verify the installation

```shell
acm --help 
```

Message `Initializing workdir` should be presented.

Add credentials file
```shell
acm add /path/to/credentails/file <alias>
```

List available aliases

```shell
acm list
```

Switch credentials file
```shell
acm use <alias>
```
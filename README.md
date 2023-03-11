## AWS Credentials manager

### Installing

Add the project executable to PATH or create an alias

```shell
alias acm='sh /<project-path>/aws-credentials-manager/apm.sh'
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
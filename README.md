# aws-rds-encrypt

[![CircleCI](https://circleci.com/gh/adamzerella/aws-rds-encrypt.svg?style=svg)](https://circleci.com/gh/adamzerella/aws-rds-encrypt)
[![GitHub stars](https://img.shields.io/github/stars/adamzerella/aws-rds-encrypt.svg)](https://github.com/adamzerella/adamzerella/stargazers)
[![GitHub license](https://img.shields.io/github/license/adamzerella/aws-rds-encrypt.svg)](https://github.com/adamzerella/adamzerella/blob/master/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/adamzerella/aws-rds-encrypt.svg)](https://github.com/adamzerella/adamzerella/issues)

> Python script to encrypt unencrypted AWS RDS instances.

Currently, [AWS RDS instances are limited when it comes to enabling encryption for existing instances](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Overview.Encryption.html#Overview.Encryption.Limitations). One must create an encrypted snapshot copy of the active instance, restore a new instance with said snapshot then redirect the active unencrypted instance to the newly created encrypted instance. This process can be confusing and time consuming, so why not automate it? 😁

> NOTE: This script relies on the RDS instance to be in the <strong>available state</strong>. Due to AWS limitations a snapshot copy cannot occur if the instance isn't available. It's reccomended to ensure <strong>no data is being written to the DB</strong> at the time of the snapshot as data loss will occur.

# Prerequisites

- [python3](https://www.python.org/downloads/)
- [pip](https://docs.python.org/3/installing/index.html#key-terms)

# Configuration

This script replies on two things to be configured prior to executing: 

1. Having a local `~/.aws/credentials` file with relevant access keys and profile names for different enviornmnets. This can be easily created using the [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/installing.html) and running `aws configure`.

2. Relevant environment variables are set:

```bash
export PROFILE_NAME="prod"                                                          # Profile name used to interact with RDS.
export RDS_KMS_ID="arn:aws:kms:us-east-1:123456:key/abcd-efgh-ijkl-mnop-qrstuvwxyz" # IAM encryption key used to encrypt RDS snapshots.
```

# Install
```python
pip3 install -r requirements.txt
```

# Start
```python
python3 src/main.py
```

Sample output should be similar to:
```text
Instance: abc                 Encrypted: False
Instance: cde                 Encrypted: True
Instance: fgh                 Encrypted: False

Detected 2 unencrypted RDS instances!
Starting RDS encryption process...

Creating snapshot for: abc
Creating encrypted snapshot from unencrypted copy
...
```

# License

This project is licensed under the MIT License - see the [LICENSE](https://raw.githubusercontent.com/adamzerella/aws-rds-encrypt/master/LICENSE) file for details.


# Contributors

<div style="display:inline;">
  <img width="64" height="64" href="https://github.com/adamzerella" src="https://avatars0.githubusercontent.com/u/1501560?s=460&v=4" alt="Adam A. Zerella"/>
</div>

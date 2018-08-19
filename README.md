# aws-rds-encrypt

[![CircleCI](https://circleci.com/gh/adamzerella/aws-rds-encrypt.svg?style=svg)](https://circleci.com/gh/adamzerella/aws-rds-encrypt)
[![GitHub stars](https://img.shields.io/github/stars/adamzerella/aws-rds-encrypt.svg)](https://github.com/adamzerella/adamzerella/stargazers)
[![GitHub license](https://img.shields.io/github/license/adamzerella/aws-rds-encrypt.svg)](https://github.com/adamzerella/adamzerella/blob/master/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/adamzerella/aws-rds-encrypt.svg)](https://github.com/adamzerella/adamzerella/issues)

> Python script to safely encrypt unencrypted AWS RDS instances with minimal downtime.

Currently, AWS don't allow RDS instances to be encrypted directly. One must create an encrypted snapshot of an active instance, restore a new instance with said snapshot then redirect the active unencrypted instance to the newly created encrypted instance. This process can be confusing and time consuming, so why not automate it? 😁

# Prerequisites

- [python3](https://www.python.org/downloads/)
- [pip](https://docs.python.org/3/installing/index.html)

# Configuration

This script replies on two things to be configured prior to executing: 

Firstly, having a local `~/.aws/credentials` file with relevant access keys and profile names for different enviornmnets. This can be easily created using the [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/installing.html) and running `aws configure`.

Secondly,  relevant environment variables are set:
```bash
export PROFILE_NAME="prod"                                                          # Profile name used to interact with RDS.
export RDS_KMS_ID="arn:aws:kms:us-east-1:123456:key/abcd-efgh-ijkl-mnop-qrstuvwxyz" # IAM encryption key used to encrypt RDS snapshots.
```

# Install
```python
pip install -r requirements.txt
```

# Start
```python
python src/main.py
```

# License

This project is licensed under the MIT License - see the [LICENSE](https://raw.githubusercontent.com/adamzerella/aws-rds-encrypt/master/LICENSE) file for details.

# Contributors

<div style="display:inline;">
  <img width="64" height="64" href="https://github.com/adamzerella" src="https://avatars0.githubusercontent.com/u/1501560?s=460&v=4" alt="Adam A. Zerella"/>
</div>
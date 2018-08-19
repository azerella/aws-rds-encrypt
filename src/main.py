import os
import time

import boto3
import botocore

PROFILE_NAME = os.environ['PROFILE_NAME']   #The local AWS profile from ~/.aws/credentials
RDS_KMS_ID = os.environ['RDS_KMS_ID']       #AWS/KMS RDS ARN used to encrypt the RDS snapshot

def main():
    # Establish a session using local AWS credentials
    session = boto3.Session(profile_name=PROFILE_NAME)
    # Instansiate AWS RDS client
    rds_client = session.client('rds')
    # Query for all RDS instances
    response = rds_client.describe_db_instances()
    # List to store the unencrypted instnaces we want to encrypt
    unencrypted_instances = []

    # Unfornatuly we cannot filter instances for StorageEncrypted so we have to do it manually.
    for instance in response['DBInstances']:
        print('Instance: {0:36} Encrypted: {1}'.format(
            instance['DBInstanceIdentifier'], 
            instance['StorageEncrypted'])
        )
        
        if instance['StorageEncrypted'] == False:
            unencrypted_instances.append(instance)

    print('\nDetected %d unencrypted RDS instances!' % len(unencrypted_instances))

    # Do we actually have things to encrypt?
    if len(unencrypted_instances) > 0:
        print('Starting RDS encryption process...\n')

        try:
            for instance in rds_client.describe_db_instances()['DBInstances']:

                print('Creating snapshot for: %s' % instance['DBInstanceIdentifier'])
                
                rds_client.create_db_snapshot(
                    DBSnapshotIdentifier='old-unencrypted-' + instance['DBInstanceIdentifier'],
                    DBInstanceIdentifier=instance['DBInstanceIdentifier']
                )

                rds_client.get_waiter('db_snapshot_available').wait(
                    DBSnapshotIdentifier='old-unencrypted-' + instance['DBInstanceIdentifier'],
                    DBInstanceIdentifier=instance['DBInstanceIdentifier']
                )
                
                print('Creating encrypted snapshot from unencrypted copy')
                
                rds_client.copy_db_snapshot(
                    SourceDBSnapshotIdentifier='old-unencrypted-' + instance['DBInstanceIdentifier'],
                    TargetDBSnapshotIdentifier='new-encrypted-' + instance['DBInstanceIdentifier'],
                    # Specifiying KmsKeyId will encrypt the snapshot copy: 
                    # https://boto3.readthedocs.io/en/latest/reference/services/rds.html#RDS.rds_client.copy_db_snapshot
                    KmsKeyId=RDS_KMS_ID,
                    CopyTags=True
                )

                rds_client.get_waiter('db_snapshot_available').wait(
                    DBSnapshotIdentifier='new-encrypted-' + instance['DBInstanceIdentifier'],
                    DBInstanceIdentifier=instance['DBInstanceIdentifier']
                )

                print('Creating instance from encrypted snapshot')

                rds_client.restore_db_instance_from_db_snapshot(
                    DBInstanceIdentifier='encrypted-' + instance['DBInstanceIdentifier'],
                    DBSnapshotIdentifier='new-encrypted-' + instance['DBInstanceIdentifier']
                )

                rds_client.get_waiter('db_instance_available').wait(
                    DBInstanceIdentifier='encrypted-' + instance['DBInstanceIdentifier']
                )

                print('Cleaning up old snapshots and instances...')

                rds_client.delete_db_snapshot(
                    DBSnapshotIdentifier='old-unencrypted-' + instance['DBInstanceIdentifier']
                )
                
                rds_client.get_waiter('db_snapshot_deleted').wait(
                    DBSnapshotIdentifier='old-unencrypted-' + instance['DBInstanceIdentifier'],
                    WaiterConfig={
                        'Delay': 5,
                        'MaxAttempts': 30
                    }
                )

                rds_client.delete_db_snapshot(
                    DBSnapshotIdentifier='new-encrypted-' + instance['DBInstanceIdentifier']
                )
                
                rds_client.get_waiter('db_snapshot_deleted').wait(
                    DBSnapshotIdentifier='new-encrypted-' + instance['DBInstanceIdentifier'],
                    WaiterConfig={
                        'Delay': 5,
                        'MaxAttempts': 30
                    }                
                )

                rds_client.delete_db_instance(
                    DBInstanceIdentifier=instance['DBInstanceIdentifier'],
                    SkipFinalSnapshot=True
                )
                
                rds_client.get_waiter('db_instance_deleted').wait(
                    DBInstanceIdentifier=instance['DBInstanceIdentifier'],
                )
                
                print('Renaming new encrypted instance with original instance name')

                rds_client.modify_db_instance(
                    DBInstanceIdentifier='encrypted-' + instance['DBInstanceIdentifier'],
                    ApplyImmediately=True, 
                    NewDBInstanceIdentifier=instance['DBInstanceIdentifier']
                )
                
                # Workaround for: https://github.com/boto/boto3/issues/609
                time.sleep(60)

                rds_client.get_waiter('db_instance_available').wait(
                    DBInstanceIdentifier=instance['DBInstanceIdentifier']
                )

                print('RDS encryption process complete for: %s!\n' % instance['DBInstanceIdentifier'])
            print('\nENCRYPTION PROCESS COMPLETE!!! \n EXIT..')
            exit(0)
        except botocore.exceptions.ClientError as e:
            print(e.response['Error']['Code'])
            exit(1)


if __name__ == '__main__':
    main()
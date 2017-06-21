## Create DynamoDB table for storing machine status data

import boto3

dynamodb = boto3.resource('dynamodb')

table = dynamodb.create_table(
    TableName='wk2demo3',
    #Define attributes that describe key schema, N:number, S:string, B:binary
    AttributeDefinitions=[
        {
            'AttributeName': 'machine_id',
            'AttributeType': 'N'
        },
        {
            'AttributeName':'timestamp',
            'AttributeType':'S'
        }
    ],
    #Define composite primary key, HASH for partition, RANGE for sort
    KeySchema=[
        {
            'AttributeName':'machine_id',
            'KeyType':'HASH'
        },
        {
            'AttributeName':'timestamp',
            'KeyType':'RANGE'
        }
    ],
    # Service pricing determined by ProvisionedThroughput, 5 min.
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)
table.meta.client.get_waiter('table_exists').wait(TableName='wk2demo3')

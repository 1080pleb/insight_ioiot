import base64
import json

import boto3
import datetime

"""
def process_status_events(records):
    
    decoded_record_data = [base64.b64decode(record['kinesis']['data']) for record in records]
    deserialized_data = [json.loads(decoded_record) for decoded_record in decoded_record_data]

    with table.batch_writer() as batch_writer:
        for item in deserialized_data:
            # Add a processed time so we have a rough idea how far behind we are
            item['processed'] = datetime.datetime.utcnow().isoformat()
            batch_writer.put_item(Item=item)

    # Print the last item to make it easy to see how we're doing
    print(json.dumps(item))
    print('Number of records: {}'.format(str(len(deserialized_data))))

def process_prod_events(records):
    return None

"""    
def lambda_handler(event, context):
    """
    Receive a batch of events from Kinesis and insert into our DynamoDB table
    """
    print('Received request')
    item = None
    dynamo_db = boto3.resource('dynamodb')
    table = dynamo_db.Table('wk2demo3')
    """
    message = event['Records']
    if message['message_type'] == 'status':
        process_status_event(messasge['message'])
    else
        process_prod_events(message['message'])
    """
    decoded_record_data = [base64.b64decode(record['kinesis']['data']) for record in event['Records']]
    deserialized_data = [json.loads(decoded_record) for decoded_record in decoded_record_data]

    with table.batch_writer() as batch_writer:
        for item in deserialized_data:
            # Add a processed time so we have a rough idea how far behind we are
            item['processed'] = datetime.datetime.utcnow().isoformat()
            batch_writer.put_item(Item=item)

    # Print the last item to make it easy to see how we're doing
    print(json.dumps(item))
    print('Number of records: {}'.format(str(len(deserialized_data))))


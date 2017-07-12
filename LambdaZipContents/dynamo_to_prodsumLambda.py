import base64
import json
import boto3
import datetime
from botocore.exceptions import ClientError
import decimal

print('Loading function')

#Helper class to convert DyDB item to json, per AWS docs
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

def lambda_handler(event, context):
    
    dynamo_db = boto3.resource('dynamodb')
    table = dynamo_db.Table('production_volume_tracker')

    for item in event['Records']:
        timedate = item['dynamodb']['Keys']['timestamp']['S'].split('T')[0]
        timehour = item['dynamodb']['Keys']['timestamp']['S'].split('T')[1].split(':')[0]
        datehourstamp = timedate + ':' + timehour

        machine_id = int(item['dynamodb']['Keys']['machine_id']['N'])

        cumul_volume = int(item['dynamodb']['NewImage']['machine_production']['N'])
        
        try:
            response = table.put_item(
                Item={
                    'datehourstamp': datehourstamp,
                    'machine_id': machine_id,
                    'cumul_volume': cumul_volume
                },
                ConditionExpression="attribute_not_exists(cumul_volume)"
            )
            print(" Remaining time (ms): " + str(context.get_remaining_time_in_millis()) + "\n")
            
        json

        except ClientError as e:

            if e.response['Error']['Code'] == "ConditionalCheckFailedException":
                print('Stamp+machine exists, updating production...')
                response = table.update_item(
                    Key={
                        'datehourstamp': datehourstamp,
                        'machine_id': machine_id
                    },
                    UpdateExpression="set cumul_volume = cumul_volume + :val",
                    ExpressionAttributeValues={
                        ':val': cumul_volume #decimal.Decimal(cumul_volume)
                    },
                    ReturnValues="UPDATED_NEW"
                )
                print(" Remaining time (ms): " + str(context.get_remaining_time_in_millis()) + "\n")

        else:
            print('New Stamp+machine record added.')

    return 'Successfully processed {} records.'.format(len(event['Records']))

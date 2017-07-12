
import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
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
    table_from = dynamo_db.Table('wk2demo3')
    table_to = dynamo_db.Table('production_ship')

    for record in event['Records']:
        machine_id = int(record['dynamodb']['NewImage']['machine_id']['N'])
        
        new_prod = int(record['dynamodb']['NewImage']['machine_production']['N'])
        
        timestamp = record['dynamodb']['NewImage']['timestamp']['S']
        
        fe = Key('machine_id').eq(machine_id);

        #Write to new table when production above some amount
        if new_prod > 110:
            response = table_from.query(
                KeyConditionExpression = fe
            )

            counter = 0
            prod = 0
            prod_sum = 0

            for i in response['Items']:
                prod = int(i['machine_production'])
                counter += 1
                prod_sum += prod

            prod_avg = prod_sum / counter
            prod_avg = int(prod_avg)
            response_avg = table_to.put_item(
                Item = {
                    'timestamp': timestamp,
                    'machine_id': machine_id,
                    'prod_avg': prod_avg
                },
            )



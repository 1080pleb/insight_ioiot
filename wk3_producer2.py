import boto3
import json
import time
import datetime
import random
import uuid
import simdata

kinesis = boto3.client('kinesis')

""" Create kinesis stream, and wait until it is active. 
Without waiting, you will get errors when putting data into the stream
"""

stream = "wk2demo4"
kinesis = boto3.client('kinesis')
if stream not in [f for f in kinesis.list_streams()['StreamNames']]:
    print('Creating Kinesis stream %s' %  stream)
    kinesis.create_stream(StreamName=stream, ShardCount=1)
else:
    print('Kinesis stream %s exists' %  stream)
while kinesis.describe_stream(StreamName=stream)['StreamDescription']['StreamStatus'] == 'CREATING':
    time.sleep(2)

print('Stream %s created. Sending data...' % stream)

""" Call mstatus to generate faux data
"""



def generate_and_submit():
    printed = False
    while True:
        gcounter = random.randint(50,100)
        #coinflip
        coin = random.randint(0,1)
        if coin:
            records_batch = [simdata.create_machine_status() for _ in range(gcounter)]
            record_type = "status"
        else:
            records_batch = [simdata.create_machine_production() for _ in range(gcounter)]
            record_type = "production"

        request = {
            'Records': {'message_type': record_type, 'message': records_batch},
            'StreamName': stream
        }
        kinesis.put_records(**request)
        print('Batch inserted. Total records: {}'.format(str(gcounter)))
        if (not printed):
            print("=============================")
            print(request)
            print("===----------================")
            printed = True
        time.sleep(0.75)
    return

generate_and_submit()


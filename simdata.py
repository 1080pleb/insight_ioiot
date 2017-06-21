import random
import json
import datetime
import uuid
import base64

def create_machine_production():

    item = {
        'machine_id': random.randint(0,1000),
        'timestamp': datetime.datetime.utcnow().isoformat(),
        'machine_production': (100 + random.randint(-20,20)),
        'machine_operator': (random.choice(['John','Paul','George','Ringo'])),
        'unique_id': str(uuid.uuid4())
    }

    raw_data = json.dumps(item)
    encoded_data = bytes(raw_data,"utf-8")

    kinesis_record_production = {
        'Data': encoded_data,
        'PartitionKey': str(item['machine_id']),
    }

    return kinesis_record_production

def create_machine_status():
    statuses = ['Working','Pause','Fault']
    list_of_probs = [0.8, 0.15, 0.05]
    item = {
        'machine_id': random.randint(0,1000),
        'timestamp': datetime.datetime.utcnow().isoformat(),
        'machine_status': random.choices(statuses, weights=list_of_probs, k=1),
        'machine_operator': (random.choice(['John','Paul','George','Ringo'])),
        'unique_id': str(uuid.uuid4())
    }

    raw_data = json.dumps(item)
    encoded_data = bytes(raw_data,"utf-8")

    kinesis_record_status = {
        'Data': encoded_data,
        'PartitionKey': str(item['machine_id']),
    }

    return kinesis_record_status


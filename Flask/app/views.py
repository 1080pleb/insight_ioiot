#jsonify creates a json representation of the response
from flask import jsonify
from flask import request, render_template

from app import app
import boto3
from boto3.dynamodb.conditions import Key, Attr
import os
import operator
from decimal import Decimal
import json

dynamodb = boto3.resource('dynamodb')
table_prod = dynamodb.Table('production_volume_tracker')
#table_status = dynamodb.Table('machine_status')
table_ship = dynamodb.Table('production_ship')

@app.route('/')

@app.route('/get_prod')
def email():
    return render_template("get_prod.html")

@app.route('/get_prod', methods=['POST'])
def get_prod_post():
    machine_id = request.form["machine_id"]
    #datehourstamp = request.form["datehourstamp"]
    machine_id_int = int(machine_id)

    fe = Key('machine_id').eq(machine_id_int);

    print(str(machine_id_int))
    response = table_ship.query(
        KeyConditionExpression=fe
        #Key = {
        #    'machine_id': machine_id_int,
        #    'timestamp': "2017-07-10T22:32:43.197817"
        #}
    )
    
    response_list = []
    for val in response['Items']:
        response_list.append(val)
    print(response_list)
    jsonresponse = [{'machine_id': x['machine_id'], 'timestamp': x['timestamp'], 'prod_avg': x['prod_avg']} for x in response_list]
    #item = response['Items']
    #item_list = [item]
    #prod = item['cumul_volume']
    #print(jsonresponse[0])
    return render_template("get_prodop.html", output=jsonresponse)   

@app.route('/realtime')
def realtime():
    return render_template("realtime.html")

@app.route('/api/<date>/<hour>/<machine_id>')
def get_prod(date, hour, machine_id):

    prod_key = str(date) + ':' + str(hour)
    machine_id = (machine_id)

    print('Item ' + prod_key + ' is type ' + str(type(prod_key)))
    print('Item ' + machine_id + ' is type ' + str(type(machine_id)))
    machine_id = int(machine_id)
    print ('Now ' + str(machine_id) + ' is type ' + str(type(machine_id)))
    #return (str(prod_key) + " " + str(machine_id))

    response = table_prod.query(
        KeyConditionExpression=Key('machine_id').eq(machine_id)
    )

    for i in response['Items']:

        #item = response['Item']
        prod = i['cumul_volume']
        print(prod)
        return str(prod)

"""

@app.route('/production')
def get_prods():
    return render_template('production.html')

@app.route('/production', methods=['POST'])
def get_prods_post():
    stamp_day = request.form['day']
    stamp_month = request.form['month']
    stamp_year = request.form['year']
    stamp_hour = request.form['hour']
    stamp = stamp_year + stamp_month + stamp_day + ':' + stamp_hour

    response = table_prod.query(
        Key = {
            'datehourstamp': stamp,
            'machine_id': machine_id

    )
@app.route('/status')
def get_status():
    return render_template('status.html')

@app.route('/status', methods=['POST'])
def get_status_post():
    response = table_status.scan(
        FilterExpression=Attr('state').contains('Error'),
        ProjectionExpression='machine_id, state', 'timestamp',
    )

response_items = response['Items']

"""

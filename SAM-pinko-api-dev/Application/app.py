import json  
import pandas as pd
from db import connect_to_db                                                                                                        
import boto3
import csv
import io
import sys
import numpy as np

headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,X-Amz-Security-Token,Authorization,X-Api-Key,X-Requested-With,Accept,Access-Control-Allow-Methods,Access-Control-Allow-Origin,Access-Control-Allow-Headers",
    "Access-Control-Allow-Origin": '*',
    "Access-Control-Allow-Methods": "DELETE,GET,HEAD,OPTIONS,PATCH,POST,PUT",
    "X-Requested-With": "*"
}


"""connection to database"""
db = connect_to_db()

def lambda_handler(event, context):
    if event.get('body') == None:
        response = {
            "statusCode": 404,
            "headers": headers,
            "body": json.dumps({"message": "no body"}),
        }
        return response
    
    body = json.loads(event.get('body'))
    pid = body.get('pid')
    market=body.get('market')
    org_id=body.get('org_id')
    start=body.get('start')
    end=body.get('end')
    if 'pid' == None and market == None:
        return {
            "statusCode": 404,
            "headers": headers,
            "body": json.dumps({"message": "no Pid and Market"})
        }
    if pid == None and market != None:
        """ return a json response of all products pid and title on the base of market """ 
        db_obj_2 = load_from_db_2(market,org_id,start,end)
        if db_obj_2 is None:
            return {
            "statusCode": 404,
            "headers": headers,
            "body": json.dumps({"message": f"could not find the Market {market}"})
        }
        else:
            return {
                'statusCode': 200,
                "headers": headers,
                "body": json.dumps(db_obj_2)
            }
    if 'pid' != None and market != None:
        """ return a json response of product details on the base of pid and market  """ 
        db_obj = load_from_db(pid, market,org_id)
        if db_obj is None:
            return {
                "statusCode": 404,
                "headers": headers,
                "body": json.dumps({"message": f"could not find the Pid {pid}"})
            }
        else:
            return {
                'statusCode': 200,
                "headers": headers,
                "body": json.dumps(db_obj)
            }


def load_from_db(pid, market, org_id):
  pid2 = f"{org_id}_{market}_{pid}" 
  db_obj = db.get(pid2) #get the pid from database 
  if db_obj is None: return None
  json_data = json.loads(db_obj.decode('utf-8'))
  return json_data

def load_from_db_2(market,org_id,start,end):
  market2=f"{org_id}_{market}" #get the market from database 
  db_obj_2 = db.get(market2)
  if db_obj_2 is None: return None
  json_data = json.loads(db_obj_2.decode('utf-8'))
  sam=json_data.get('data')
  res_list = [sam[i] for i in range(start,end+1)]
  return res_list  


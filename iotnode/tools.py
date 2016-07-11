#coding=utf-8
#__author__ = 'zhao'

from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

from django.http import HttpResponse,JsonResponse
from iotnode.models import NodeInfo, TokenTable, NodeData,FileData
from datetime import datetime, date
import requests
import datetime
from check_validity import Check_validity
import json

CLOUD_MAC = '0A1B2C3D'
SERVICE_TYPE = 0
SECURITY_LEVEL= 6
URL_REGISTER_TOKEN = 'http://127.0.0.1:9000/requesttoken/'
URL_UPDATE_TOKEN = 'http://127.0.0.1:9000/updatetoken/'
URL_DEL_USER='http://127.0.0.1:9000/deleteuser/'
SERVICE_LIMITATION=30 #30 DAYS
TOKEN_EXPIRE=1 #1 DAY

def Create_token(payload,node_id):
    req_token=requests.post(URL_REGISTER_TOKEN,data=payload)
    print req_token.status_code
    responsejson=req_token.json()
    #print responsejson,type(responsejson)
    response_token=responsejson['token']
    response_priority=responsejson['priority']
    response_service_type=responsejson['service_type']
    response_service_limitation=responsejson['service_limitation']
    response_token_start = responsejson['token_start']
    response_timestamp=responsejson['timestamp']
    response_token_security_level=responsejson['token_security_level']
    #print response_token
    #print node_id#,dir(NodeInfo.objects.get(node_mac=node_mac_get))
    create_token=TokenTable()
    create_token.node_id=node_id
    create_token.token=response_token
    create_token.priority=response_priority
    create_token.service_type=response_service_type
    create_token.service_limitation=response_service_limitation
    create_token.token_security_level=response_token_security_level
    create_token.token_start = response_token_start
    create_token.timestamp=response_timestamp
    #print create_token.token,create_token.node_id
    create_token.save()
    JsonDict={
        "token":response_token,"priority":response_priority,
        "service_type":response_service_type,
        "service_limitation":response_service_limitation,
        'token_start':response_token_start,
        'timestamp':response_timestamp,
        'token_security_level':response_token_security_level,
        'del_signal':0,
        'return_code':200
            }
    #print JsonDict
    return  JsonDict

def Del_user(payload,object):
    req_del = requests.post(URL_DEL_USER, data=payload)
    print req_del.status_code
    responsejson = req_del.json()
    print responsejson,type(responsejson)
    #response_del_user=responsejson['del_num']
    response_del_user = responsejson['del_signal']
    if response_del_user:
        del_num=object.delete()
    return del_num
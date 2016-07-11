#coding=utf-8
#__author__ = 'zhao'

from iotnode.models import NodeInfo, TokenTable, NodeData
from datetime import datetime, date
import requests
import datetime

CLOUD_MAC = '0A1B2C3D'
SERVICE_TYPE = 0
URL_REGISTER_TOKEN = 'http://127.0.0.1:9000/requesttoken/'
URL_UPDATE_TOKEN = 'http://127.0.0.1:9000/updatetoken/'
SERVICE_LIMITATION=30 #30 DAYS
TOKEN_EXPIRE=1 #1 DAY

class Check_validity(object):
    def __init__(self,timestamp,token_start,service_limitation):
        self.timestamp=timestamp
        self.token_start=token_start
        self.service_limitation = service_limitation


    def check_token_expire(self):
        t0=datetime.datetime.now()
        #a=self.token_start+datetime.timedelta(minutes=120)
        diff=t0>=(self.token_start+datetime.timedelta(minutes=1))#設置爲2小時後失效
        #print diff,a
        if diff:
            expired=1 #超时
        else:
            expired=0 #剩余时间多于1天
        return expired

    def check_service_expire(self):
        t0=datetime.datetime.now()
        #a=self.token_start+datetime.timedelta(minutes=120)
        diff=t0>=(self.timestamp+datetime.timedelta(days=1))#self.service_limitation))#設置爲30days後失效

        if diff:
            service_expired = 1  # 超时
        else:
            service_expired = 0
        return service_expired



    def update_token(self,payload,node_id):
        req_token = requests.post(URL_UPDATE_TOKEN, data=payload)
        print req_token.status_code,11
        responsejson = req_token.json()
        print responsejson, type(responsejson)
        if responsejson['del_signal']==11:
            update_num = TokenTable.objects.filter(token=payload['node_token']).delete()
        else:
            response_token = responsejson['token']
            #response_priority = responsejson['priority']
            #response_service_type = responsejson['service_type']
            #response_service_limitation = responsejson['service_limitation']
            response_token_start = responsejson['token_start']
            #response_timestamp = responsejson['timestamp']
            #print response_token,response_token_start
            update_num=TokenTable.objects.filter(token=payload['node_token']).update(token=response_token,token_start=response_token_start)
            print update_num
        return update_num,responsejson

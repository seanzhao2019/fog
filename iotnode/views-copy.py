#coding=utf-8
#__author__ = 'zhao'

from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,JsonResponse
from iotnode.models import NodeInfo, TokenTable, NodeData
from datetime import datetime, date
import requests
import datetime
from check_validity import Check_validity
import json
# Create your views here.
CLOUD_MAC = '0A1B2C3D'
SERVICE_TYPE = 0
URL_REGISTER_TOKEN = 'http://127.0.0.1:9000/request_token/'
URL_UPDATE_TOKEN = 'http://127.0.0.1:9000/update_token/'
URL_DEL_USER='http://127.0.0.1:9000/del_user/'
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
    #print response_token
    #print node_id#,dir(NodeInfo.objects.get(node_mac=node_mac_get))
    create_token=TokenTable()
    create_token.node_id=node_id
    create_token.token=response_token
    create_token.priority=response_priority
    create_token.service_type=response_service_type
    create_token.service_limitation=response_service_limitation
    create_token.token_start = response_token_start
    create_token.timestamp=response_timestamp
    #print create_token.token,create_token.node_id
    create_token.save()
    JsonDict={"token":response_token,"priority":response_priority,"service_type":response_service_type,
                             "service_limitation":response_service_limitation,
              'token_start':response_token_start,'timestamp':response_timestamp,'del_signal':0
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

@csrf_exempt
def Register_NodeInfo(request):

    try:
        if request.method=='POST':
            #print request.POST

            node_mac_get=request.POST.get('node_mac')
            node_user_get=request.POST.get('node_user')
            service_limitation_get = request.POST.get('service_limitation')
            #print (node_mac_get)
            get_nodeinfo=NodeInfo.objects.get_or_create(node_mac=node_mac_get,node_user=node_user_get,
                                                        defaults={'service_limitation': service_limitation_get})
            #print get_nodeinfo[0],type(get_nodeinfo[0])
            #print hasattr(update_nodeinfo[0],'pk')
            node_id = get_nodeinfo[0].pk

            if get_nodeinfo[1]==True:
                print node_id,1
                payload={
                    'node_mac' : node_mac_get,
                    'node_user' : node_user_get,
                    'cloud_mac': CLOUD_MAC,
                    'service_limitation':service_limitation_get,
                    'timestamp':get_nodeinfo[0].timestamp
                }
                print payload
                JsonDict=Create_token(payload,node_id)
                #print JsonDict

                return JsonResponse(JsonDict)
            else:
                print node_id,2
                try:
                    Token_node=TokenTable.objects.get(node_id=node_id)
                    node_token=Token_node.token
                    #print node_token
                    node_priority=Token_node.priority
                    node_service_type=Token_node.service_type
                    node_service_limitation=Token_node.service_limitation
                    node_token_start=Token_node.token_start
                    node_timestamp=Token_node.timestamp
                    #print node_token_start
                    check_update=Check_validity(node_timestamp,node_token_start,node_service_limitation)
                    check_token_expired=check_update.check_token_expire()
                    check_service_expired= check_update.check_service_expire()
                    print check_service_expired
                    if check_service_expired:
                        payload = {
                            'node_mac': get_nodeinfo[0].node_mac,
                            'node_user': get_nodeinfo[0].node_user,
                        }
                        del_user=Del_user(payload,get_nodeinfo[0])
                        JsonDict={
                            'del_user':del_user
                        }
                    else:
                        if check_token_expired:
                            payload = {
                                #'node_mac': node_mac_get,
                                #'node_user': node_user_get,
                                #'cloud_mac': CLOUD_MAC
                                'node_token': node_token
                            }
                            print payload
                            update_num,ResponDict=check_update.update_token(payload,node_id)
                            #print update_num
                            if update_num:
                                JsonDict=ResponDict
                        else:
                            JsonDict={"token":node_token,"priority":node_priority,"service_type":node_service_type,
                                 "service_limitation":node_service_limitation,"token_start":node_token_start,
                                  'timestamp':node_timestamp,'del_signal':0
                                 }
                except ObjectDoesNotExist:
                    print 'oook',node_id,3
                    payload={
                    'node_mac' : get_nodeinfo[0].node_mac,
                    'node_user' : get_nodeinfo[0].node_user,
                    'cloud_mac': CLOUD_MAC,
                    'service_limitation':get_nodeinfo[0].service_limitation,
                    'timestamp':get_nodeinfo[0].timestamp
                    }
                    print payload
                    JsonDict=Create_token(payload,node_id)

                return JsonResponse(JsonDict)

    except:
        print 'something wrong'

    return HttpResponse('ERROR')

@csrf_exempt
def Update_Service(request):

    try:
        if request.method=='POST':
            #print request.POST

            node_token_get=request.POST.get('node_token')
            node_event_get=request.POST.get('node_event')
            tokeninfo=TokenTable.objects.get(token=node_token_get)
            tokeninfo_service_type=tokeninfo.service_type
            tokeninfo_service_limitation = tokeninfo.service_limitation
            tokeninfo_priority=tokeninfo.priority
            tokeninfo_token_start = tokeninfo.token_start
            tokeninfo_timestamp = tokeninfo.timestamp
            check_token=Check_validity(tokeninfo_timestamp,tokeninfo_token_start,tokeninfo_service_limitation)
            check_service_expired=check_token.check_service_expire()
            check_token_expired=check_token.check_token_expire()
            if check_service_expired:
                pass
            else:
                if check_token_expired:
                    payload = {
                        # 'node_mac': node_mac_get,
                        # 'node_user': node_user_get,
                        # 'cloud_mac': CLOUD_MAC
                        'node_token': node_token_get
                    }
                    update_num, ResponDict = check_update.update_token(payload, node_id)
                    # print update_num
                    if update_num:
                        JsonDict = ResponDict
        return HttpResponse('ERROR')

    except:
        print 'something wrong'

    return HttpResponse('ERROR')



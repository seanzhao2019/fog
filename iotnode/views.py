#coding=utf-8
#__author__ = 'zhao'

from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,JsonResponse
from iotnode.models import NodeInfo, TokenTable, NodeData,FileData
from datetime import datetime, date
import requests
import datetime
from check_validity import Check_validity
from tools import *
import logging
import json
# Create your views here.
CLOUD_MAC = '0A1B2C3D'
SERVICE_TYPE = 0
SECURITY_LEVEL= 6
URL_REGISTER_TOKEN = 'http://127.0.0.1:9000/request_token/'
URL_UPDATE_TOKEN = 'http://127.0.0.1:9000/update_token/'
URL_DEL_USER='http://127.0.0.1:9000/del_user/'
SERVICE_LIMITATION=30 #30 DAYS
TOKEN_EXPIRE=1 #1 DAY



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
                        JsonDict={
                            "token":node_token,"priority":node_priority,
                            "service_type":node_service_type,"service_limitation":node_service_limitation,
                            "token_start":node_token_start,'timestamp':node_timestamp,
                            'del_signal':0,'return_code':200
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
                payload = {
                    'node_mac': get_nodeinfo[0].node_mac,
                    'node_user': get_nodeinfo[0].node_user,
                }
                del_user = Del_user(payload, get_nodeinfo[0])
                JsonDict = {
                    'del_user': del_user
                }
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


@csrf_exempt
def Update_Sensordata(request):

    try:
        if request.method=='POST':
            #print request.POST

            node_token_get=request.POST.get('node_token')
            node_longitude_get=request.POST.get('node_longitude')
            node_latitude_get = request.POST.get('node_latitude')
            node_heart_rate_get=request.POST.get('node_heart_rate')
            node_energy_state_get=request.POST.get('node_energy_state')

            node_pk=TokenTable.objects.get(token=node_token_get).pk
            create_nodedata=NodeData()
            create_nodedata.node_id=node_pk
            create_nodedata.longitude=node_longitude_get
            create_nodedata.latitude = node_latitude_get
            create_nodedata.heart_rate=node_heart_rate_get
            create_nodedata.energy_state=node_energy_state_get
            create_nodedata.save()

            JsonDict = {
                'return_code':200
            }
        return JsonResponse(JsonDict)

    except:
        print 'something wrong'

    return HttpResponse('ERROR')

@csrf_exempt
def Update_Priority(request):

    try:
        if request.method=='POST':
            #print request.POST

            node_token_get=request.POST.get('node_token')
            node_priority_get=request.POST.get('node_priority')


            update_token=TokenTable.objects.get(token=node_token_get)
            update_token.priority=node_priority_get
            update_token.save()

            JsonDict = {
                'return_code':200
            }
        return JsonResponse(JsonDict)

    except:
        print 'something wrong'

    return HttpResponse('ERROR')

@csrf_exempt
def Get_Priority(request):

    try:
        if request.method=='POST':
            #print request.POST

            node_token_get=request.POST.get('node_token')

            priority=TokenTable.objects.get(token=node_token_get).priority

            JsonDict = {
                'return_code':200,
                'priority':priority
            }
        return JsonResponse(JsonDict)

    except:
        print 'something wrong'

    return HttpResponse('ERROR')

@csrf_exempt
def Update_Token(request):

    try:
        if request.method=='POST':
            #print request.POST

            node_token_get=request.POST.get('node_token')


            node_pk=TokenTable.objects.get(token=node_token_get).pk
            node_timestamp=TokenTable.objects.get(token=node_token_get).timestamp
            node_token_start=TokenTable.objects.get(token=node_token_get).token_start
            node_service_limitation=TokenTable.objects.get(token=node_token_get).service_limitation
            payload = {
                'node_token': node_token_get
            }
            print payload
            try:
                check_update = Check_validity(node_timestamp, node_token_start, node_service_limitation)
                update_num, ResponDict = check_update.update_token(payload, node_pk)
            except Exception as e:
                logging.exception(e)

            JsonDict = {
                'return_code':200,
                'update_num':update_num
            }
        return JsonResponse(JsonDict)

    except:
        print 'something wrong'

    return HttpResponse('ERROR')

@csrf_exempt
def Update_Service_Type(request):

    try:
        if request.method=='POST':
            #print request.POST

            node_token_get=request.POST.get('node_token')
            node_service_type_get=request.POST.get('node_service_type')


            update_token=TokenTable.objects.get(token=node_token_get)
            update_token.service_type=node_service_type_get
            update_token.save()

            JsonDict = {
                'return_code':200
            }
        return JsonResponse(JsonDict)

    except:
        print 'something wrong'

    return HttpResponse('ERROR')

@csrf_exempt
def Get_Service_Type(request):

    try:
        if request.method=='POST':
            #print request.POST

            node_token_get=request.POST.get('node_token')

            service_type=TokenTable.objects.get(token=node_token_get).service_type

            JsonDict = {
                'return_code':200,
                'service_type':service_type
            }
        return JsonResponse(JsonDict)

    except:
        print 'something wrong'

    return HttpResponse('ERROR')

@csrf_exempt
def Update_Token_Security_Level(request):

    try:
        if request.method=='POST':
            #print request.POST

            node_token_get=request.POST.get('node_token')
            node_token_security_level_get=request.POST.get('node_token_security_level')


            update_token=TokenTable.objects.get(token=node_token_get)
            update_token.token_security_level=node_token_security_level_get
            update_token.save()

            JsonDict = {
                'return_code':200
            }
        return JsonResponse(JsonDict)

    except:
        print 'something wrong'

    return HttpResponse('ERROR')


@csrf_exempt
def Get_Token_Security_Level(request):

    try:
        if request.method=='POST':
            #print request.POST

            node_token_get=request.POST.get('node_token')

            token_security_level=TokenTable.objects.get(token=node_token_get).token_security_level

            JsonDict = {
                'return_code':200,
                'token_security_level':token_security_level
            }
        return JsonResponse(JsonDict)

    except:
        print 'something wrong'

    return HttpResponse('ERROR')

@csrf_exempt
def Upload_File(request):

    try:
        if request.method=='POST':
            print request.POST

            node_token_get=request.POST.get('node_token')
            node_file_get=request.FILES.get('node_file')

            print node_token_get,node_file_get
            print dir(node_file_get),type(node_file_get)
            print node_file_get.file

            node_id=TokenTable.objects.get(token=node_token_get).pk
            print node_id
            create_file=FileData()
            create_file.node_id=node_id
            try:
                create_file.file=node_file_get

                create_file.save()
            except Exception as e:
                logging.exception(e)

            JsonDict = {
                'return_code':200
            }
        return JsonResponse(JsonDict)

    except:
        print 'something wrong'

    return HttpResponse('ERROR')
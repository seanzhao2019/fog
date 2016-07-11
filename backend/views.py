from django.core.paginator import  Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render,get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from iotnode.models import NodeInfo, TokenTable, NodeData,FileData
import datetime
# Create your views here.
@csrf_exempt
def Admin_detail(request,node_id):
    node_info = get_object_or_404(NodeInfo,pk=node_id)
    #print node_info.pk
    token_info =TokenTable.objects.get(node_id=node_id)
    #print token_info,type(token_info)
    try:
        node_data = NodeData.objects.get(node_id=node_id)
        #print node_data
        return render(request, 'backend/index.html',{"node_info": node_info,
                                                     "node_data": node_data,
                                                     "token_info": token_info})
    except:
        return render(request, 'backend/index.html',{"node_info": node_info,
                                                     "token_info": token_info})


@csrf_exempt
def Api_iot(request):
    return render(request, 'backend/api.html')

@csrf_exempt
def Acc_manager(request):
    return render(request, 'backend/acc-m.html')

@csrf_exempt
def Login(request):
    return render(request, 'backend/login.html')

@csrf_exempt
def List_user(request):
    iot_node_list = NodeInfo.objects.all()
    register_code=[]
    for i in iot_node_list:
        now = datetime.datetime.now()
        if now <= (i.timestamp+datetime.timedelta(days=i.service_limitation)):
            status_code = 1
        else:
            status_code = 0
        register_code.append(status_code)
    paginator = Paginator(iot_node_list,10)
    page = request.GET.get('page')

    try:
        node_show = paginator.page(page)
    except PageNotAnInteger:
        node_show = paginator.page(1)
    except EmptyPage:
        node_show = paginator.page(paginator.num_pages)

    return render(request, 'backend/node-list.html', {'node_show':node_show,'register_code':register_code})
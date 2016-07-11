from django.contrib import admin
from iotnode.models import NodeInfo, TokenTable, NodeData,FileData
# Register your models here.
class NodeInfoAdmin(admin.ModelAdmin):
    list_display = ('node_mac','node_user')

class TokenTableAdmin(admin.ModelAdmin):
    list_display = ('node','token','priority','service_type','service_limitation','token_security_level','token_start','timestamp')

class NodeDataAdmin(admin.ModelAdmin):
    list_display = ('node','heart_rate','energy_state','longitude','latitude','update_time')

class FileAdmin(admin.ModelAdmin):
    list_display = ('node','file')
admin.site.register(NodeInfo, NodeInfoAdmin)
admin.site.register(TokenTable, TokenTableAdmin)
admin.site.register(NodeData, NodeDataAdmin)
admin.site.register(FileData, FileAdmin)
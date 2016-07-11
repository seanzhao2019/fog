from __future__ import unicode_literals

from django.db import models

# Create your models here.
class NodeInfo(models.Model):
    node_mac=models.CharField(max_length=30)
    node_user=models.CharField(max_length=30)
    service_limitation = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together=(("node_mac","node_user"),)
        ordering = ['-timestamp']

    def __unicode__(self):
        return unicode(self.node_mac)

class TokenTable(models.Model):
    node=models.OneToOneField(NodeInfo)
    token=models.CharField(max_length=32,unique=True)
    priority=models.IntegerField()
    service_type=models.IntegerField()
    service_limitation=models.IntegerField()
    token_security_level=models.CharField(max_length=20)
    token_start=models.DateTimeField()
    timestamp=models.DateTimeField()

    def __unicode__(self):
        return unicode(self.node)



class NodeData(models.Model):
    node=models.ForeignKey(NodeInfo,on_delete=models.CASCADE)
    heart_rate=models.IntegerField(null=True)
    energy_state=models.IntegerField(null=True)
    longitude=models.FloatField(null=True)
    latitude=models.FloatField(null=True)
    update_time=models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode(self.node)

class FileData(models.Model):
    node=models.ForeignKey(NodeInfo,on_delete=models.CASCADE)
    file=models.FileField(upload_to='uploads/%Y/%m/%d')

    def __unicode__(self):
        return unicode(self.node)
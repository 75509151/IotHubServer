import shortuuid


from django.shortcuts import render
from django.conf import settings
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.exceptions import  NotFound
from rest_framework.status import HTTP_201_CREATED

from utils.utils import gen_condition
from utils.res import JsonResponse
from .models import Device, DeviceAcl, Connections
from .serializers import DeviceSerializer
# Create your views here.

class DeviceView(mixins.CreateModelMixin,
                mixins.ListModelMixin,
                mixins.DestroyModelMixin,
                viewsets.GenericViewSet):

    def list(self, request):
        filter_params = ["product_name", "device_name",
                         "status", "device_status"]
        condition = gen_condition(request.query_params, filter_params)

        devices = Device.find(condition)
        if devices:
            serialized = DeviceSerializer(devices, many=True)
            return JsonResponse(serialized.data)
        else:
            return NotFound()

    def create(self, request):
        product_name = request.data["product_name"]
        device_name = shortuuid.uuid()
        password = shortuuid.uuid()
        username = "%s/%s" % (product_name, device_name)

        new_device = Device(product_name,
                            device_name,
                            username,
                            password)
        device_doc = new_device.to_doc()

        Device.insert_one(device_doc)

        acl = new_device.get_acl()
        acl["username"] = new_device.username
        device_acl = DeviceAcl(**acl)

        DeviceAcl.insert_one(device_acl.to_doc())
        serialized = DeviceSerializer(device_doc)
        return JsonResponse(serialized.data, status=HTTP_201_CREATED)

    def delete(self, request):
        #TODO:
        #踢出在线设备, 删除信息， 删除连接，删除acl
        filter_params = ["product_name", "device_name"]
        condition = gen_condition(request.query_params, filter_params, not_empty=True)
        device = Device.find_one(condition)
        if device:
            d = Device(**device)
            d.disconnect()
            d.remove()
            serialized = DeviceSerializer(device)
            return JsonResponse(serialized.data)
        else:
            raise NotFound()








import shortuuid
from django.shortcuts import render
from django.conf import settings
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.response import Response

from utils.utils import gen_condition
from .models import Device
from .serializers import DeviceSerializer
# Create your views here.

class DeviceView(mixins.CreateModelMixin,
                 mixins.RetrieveModelMixin,
                 mixins.ListModelMixin,
                viewsets.GenericViewSet):

    def list(self, request):
        filter_params = ["product_name", "device_name",
                         "status", "device_status"]
        condition = gen_condition(request.query_params, filter_params)

        device = Device.find(condition)
        serialized = DeviceSerializer(device, many=True)
        return Response(serialized.data)


    def retrieve(self, request, pk=None):
        device = Device.find_one()

        serialized = DeviceSerializer(device)
        return Response(serialized.data)

    def create(self, request):
        product_name = request.data["product_name"]
        device_name = shortuuid.uuid()
        password = shortuuid.uuid()
        username = "%s/%s" % (product_name, device_name)

        new_device = Device(product_name,
                            device_name,
                            username,
                            password)
        doc = new_device.to_doc()

        Device.insert_one(doc)
        serialized = DeviceSerializer(doc)
        return Response(serialized.data)



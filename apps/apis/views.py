import shortuuid
from django.shortcuts import render
from django.conf import settings
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.response import Response

from utils.mongo import Mongo
from .models import Device
from .serializers import DeviceSerializer
# Create your views here.

client = Mongo(settings.MONGO_URL, settings.MONGO_PORT)

mqtt_db = client.mqtt
devices_clec =  mqtt_db.devices


class DeviceView(mixins.ListModelMixin, viewsets.GenericViewSet):

    def post(self, request):
        product_name = request.data["product_name"]
        device_name = shortuuid.uuid()
        password = shortuuid.uuid()
        username = "%s/%s" % (product_name, device_name)

        new_device = Device(product_name,
                            device_name,
                            username,
                            password)

        devices_clec.insert_one(new_device.to_doc())
        serialized = DeviceSerializer(new_device.to_doc())
        return Response(serialized.data)



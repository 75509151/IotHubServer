from rest_framework import serializers

from .models import Device, Connections


class DeviceSerializer(serializers.Serializer):
    device_name = serializers.CharField()
    username = serializers.CharField()
    password = serializers.CharField()
    status = serializers.CharField()
    device_status = serializers.CharField()
    last_status_update = serializers.TimeField() #("最新更新时间")
    tags = serializers.ListField()
    shadow = serializers.JSONField()
    # shadow = serializers.DictField()

    def create(self, attrs, instance=None):
        if instance:
            instance.product_name = attrs.get('product_name', instance.product_name)
            instance.device_name = attrs.get("device_name", instance.device_name)
            instance.username = attrs.get('username', instance.username)
            instance.password = attrs.get('password', instance.password)
            instance.status = attrs.get("status", instance.status)
            instance.device_status = attrs.get("device_status", instance.device_status)
            instance.last_status_update = attrs.get("last_status_update", instance.last_status_update)
            instance.tags = attrs.get("tags", instance.tags)
            instance.tags_version = attrs.get("tags_version", instance.tags_version)
            instance.shadow = attrs.get("shadow", instance.shadow)

            return instance
        return Device(attrs.get("product_name"),
                      attrs.get("device_name"),
                      attrs.get("username"),
                      attrs.get("password"))


class ConnectionsSerializer(serializers.Serializer):
    clinet_id = serializers.CharField()
    device = serializers.CharField()
    connected = serializers.BooleanField()
    keepalive = serializers.IntegerField()
    connected_at = serializers.DateTimeField()


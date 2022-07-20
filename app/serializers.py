from rest_framework import serializers
from rest_framework.serializers import Serializer, FileField, ListField


class DoAssetAttributionSerializer(serializers.Serializer):
    file_uploaded = FileField()
    inputFile = serializers.CharField()
    outputDir = serializers.CharField()
    class Meta:
        fields = ['file_uploaded','inputFile','outputDir']


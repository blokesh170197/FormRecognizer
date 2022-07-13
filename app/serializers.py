from rest_framework import serializers
from rest_framework.serializers import Serializer, FileField, ListField


# Serializers define the API representation.
class UploadSerializer(Serializer):
    file_uploaded = FileField()
    class Meta:
        fields = ['file_uploaded']


class doAssetAttributionSerializer(serializers.Serializer):
    inputFile = serializers.CharField()
    outputDir = serializers.CharField()

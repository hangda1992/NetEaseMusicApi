from rest_framework import serializers


class SearchSongSerializer(serializers.Serializer):
    page = serializers.IntegerField(required=True, max_value=9999, min_value=1)
    keyword = serializers.CharField(required=True, allow_blank=True, max_length=50)


class Mp3UrlSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)

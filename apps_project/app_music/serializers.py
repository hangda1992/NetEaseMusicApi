from rest_framework import serializers


class SearchSongSerializer(serializers.Serializer):
    page = serializers.IntegerField(required=True, max_value=9999, min_value=1)
    keyword = serializers.CharField(required=True, allow_blank=True, max_length=50)


class MusicMp3Serializer(serializers.Serializer):
    song_id = serializers.CharField(required=True, max_length=99)

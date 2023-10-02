from rest_framework.serializers import ModelSerializer

from .models import Video

class VideoSerializer(ModelSerializer):
    class Meta:
        model = Video
        fields = [
            'name', 
            'file',
        ]


class GetAllVideosSerializer(ModelSerializer):
    class Meta:
        model = Video
        fields = [
            'id',
            'name',
            'url',
        ]

class GetVideoSerializer(ModelSerializer):
    class Meta:
        model = Video
        fields = [
            'id',
            'name',
            'file',
            'transcription',
            'created_at'
        ]
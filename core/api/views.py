from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from django.http import Http404, FileResponse
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from .models import Video
from .serializers import VideoSerializer, GetAllVideosSerializer, GetVideoSerializer
from .utils import transcribeVideo

# Create your views here.

class VideoGetUpload(APIView):

    parser_classes = [MultiPartParser, FormParser]

    def get_object(self, pk):
        try:
            return Video.objects.get(pk=pk)
        except Video.DoesNotExist:
            raise Http404

    def get(self, request, id):
        video = self.get_object(id)
        # print(video.file)
        # print(video.file.file)
        # serializer = GetVideoSerializer(video)
        # data = {
        #     "id":video.id,
        #     "name":video.name,
        #     "video":video.file.file,
        #     "transcription":video.transcription,
        #     "created_at":video.created_at
        # }
        video_file = video.file.file
        response = FileResponse(video_file, content_type='video/mp4')
        response['Content-Disposition'] = f'attachment; filename="{video_file.name}"'
        return response
    
    def post(self, request):
        serializer = VideoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        video_file = serializer.save()
        domain = request.build_absolute_uri('/')
        video_file.url = domain + 'api/video/' + str(video_file.id)
        video_file.save()

        data = {
            "id": video_file.id,
            "name": video_file.name,
            "url": video_file.url
        }
        return Response(data=data)
    
    def put(self, request, id):
        video = self.get_object(id)

        try:
            video_blob = request.data['blob']

            if video_blob == 'END':
                # Transcribe video
                path = video.file.path
                text = transcribeVideo(path)
                video.transcription = text
                video.save()
                data = {
                    "status":"Video transcribed",
                    "transcription":video.transcription
                }
                return Response(data=data)
                

            else:
                video.file.close()
                with default_storage.open(video.file.name, 'ab') as f:
                    f.write(video_blob.read())
                    f.close()


        except KeyError:
            data = {"error":"Blob not found in the request"}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            data = {"error":str(e)}
            return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(
            data={"status":"Blob recieved successfully."},
            status=status.HTTP_200_OK
        )


class GetVideos(generics.ListAPIView):
    queryset = Video.objects.all()
    serializer_class = GetAllVideosSerializer

from django.urls.conf import path

from .views import *

urlpatterns = [
    path('video/', VideoGetUpload.as_view()),
    path('videos/', GetVideos.as_view()),
    path('video/<uuid:id>', VideoGetUpload.as_view()),
    path('video/play/<uuid:id>', PlayVideo.as_view())
]

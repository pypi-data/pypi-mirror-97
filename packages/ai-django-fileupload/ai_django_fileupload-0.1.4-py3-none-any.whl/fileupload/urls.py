from django.conf.urls import url
from fileupload import views

urlpatterns = [

    url(r'^new/$', views.AttachmentCreateView.as_view(), name='upload-new'),
    url(r'^delete/(?P<pk>\d+)$', views.AttachmentDeleteView.as_view(), name='upload-delete'),
    url(r'^view/$', views.AttachmentListView.as_view(), name='upload-view')

]

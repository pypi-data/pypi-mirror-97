import json
import os

from django.conf import settings
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView
from fileupload.mixins import CustomAccessMixin

from .models import Attachment
from .response import JSONResponse, response_mimetype
from .serialize import serialize


class AttachmentForm(ModelForm):

    class Meta:
        model = Attachment
        fields = "__all__"

    def clean_file(self):
        data = self.cleaned_data['file']
        extension = os.path.splitext(data.name)[1]
        if hasattr(settings, 'UPLOADER_ALLOW_FILETYPE'):
            if extension not in settings.UPLOADER_ALLOW_FILETYPE:
                if hasattr(settings, 'UPLOADER_ALLOW_FILETYPE_ERROR_MESSAGE'):
                    raise ValidationError(_(settings.UPLOADER_ALLOW_FILETYPE_ERROR_MESSAGE))
                raise ValidationError(_(f'The file extension {extension} is not supported'))
        if hasattr(settings, 'UPLOADER_DISALLOW_FILETYPE'):
            if extension in settings.UPLOADER_DISALLOW_FILETYPE:
                if hasattr(settings, 'UPLOADER_DISALLOW_FILETYPE_ERROR_MESSAGE'):
                    raise ValidationError(_(settings.UPLOADER_DISALLOW_FILETYPE_ERROR_MESSAGE))
                raise ValidationError(_(f'The file extension {extension} is not supported'))
        return data


class AttachmentCreateView(CustomAccessMixin, CreateView):
    form_class = AttachmentForm

    def form_valid(self, form):
        self.object = form.save()
        files = [serialize(self.object)]
        data = {'files': files}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        # response = HttpResponse(json.dumps(data), content_type="application/json")
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response

    def form_invalid(self, form):
        data = json.dumps(form.errors)
        return HttpResponse(content=data, status=400, content_type='application/json')


class AttachmentDeleteView(CustomAccessMixin, DeleteView):
    model = Attachment

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        response = JSONResponse(True, mimetype=response_mimetype(request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response


class AttachmentListView(CustomAccessMixin, ListView):
    model = Attachment

    def render_to_response(self, context, **response_kwargs):
        files = [serialize(p) for p in self.get_queryset().filter(content_type=self.request.GET['content_type_id'],
                                                                  object_id=self.request.GET['object_id'])]

        data = {'files': files}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response

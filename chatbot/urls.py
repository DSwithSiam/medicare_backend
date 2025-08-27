from django.urls import path
from .views import upload_document, chat_with_doc

from django.urls import path
 
urlpatterns = [
    path("upload/", upload_document, name="upload_document"),
    path("chat/", chat_with_doc, name="chat_with_doc"),
]
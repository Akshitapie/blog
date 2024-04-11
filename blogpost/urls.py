from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("details/<int:id>/", views.details, name="details"),
    path("add", views.add, name="add"),
    path("insert", views.insert, name="insert"),
    path("alldatablog", views.alldatablog, name="alldatablog"),
    path("allpost", views.allpost, name="allpost"),
    path("addpost", views.addpost, name="addpost"),
    path("insertpost", views.insertpost, name="insertpost"),
    path("update/<int:id>/", views.update, name="update"),
    path("update/edit/<int:id>/", views.edit, name="edit"),
    path("tag", views.tag, name="tag"),
    path("addtag", views.addtag, name="addtag"),
    path("latestblog", views.latestblog, name="latestblog"),
    path("categorywise/<int:id>/", views.categorywise, name="categorywise"),
    path("mateview", views.mateview, name="mateview"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

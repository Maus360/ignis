from django.urls import path
from django.contrib.auth.decorators import login_required
from ignis import views

urlpatterns = [
    path("", views.index, name="index"),
    path("dataset/", views.DatasetListView.as_view(), name="dataset-list"),
    path(
        "dataset/create",
        login_required(views.DatasetCreateView.as_view()),
        name="dataset-create",
    ),
    path("dataset/<int:pk>", views.DatasetDetailView.as_view(), name="dataset-detail"),
    path(
        "dataset/<int:pk>/delete",
        login_required(views.DatasetDeleteView.as_view()),
        name="dataset-delete",
    ),
    path(
        "dataset/<int:pk>/update",
        login_required(views.DatasetUpdateView.as_view()),
        name="dataset-update",
    ),
    path("nn/", views.NNListView.as_view(), name="nn-list"),
    path("nn/create", login_required(views.NNCreateView.as_view()), name="nn-create"),
    path("nn/<int:pk>", views.NNDetailView.as_view(), name="nn-detail"),
    path(
        "nn/<int:pk>/delete",
        login_required(views.NNDeleteView.as_view()),
        name="nn-delete",
    ),
    path(
        "nn/<int:pk>/update",
        login_required(views.NNUpdateView.as_view()),
        name="nn-update",
    ),
    path("signup/", views.SignUpView.as_view(), name="signup"),
]

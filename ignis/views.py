from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from datetime import datetime
import logging

from ignis.models import *
from ignis.forms import *

from engine import tool

logger = logging.getLogger("ignis")


def index(request):
    """
    View function for home page of site.
    """
    # Render the HTML template index.html
    return render(request, "index.html")


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("index")
    template_name = "registration/signup.html"


class DatasetListView(generic.ListView):
    """
    Generic class-based view for a list of all blogs.
    """

    model = Dataset
    paginate_by = 15


class DatasetDetailView(generic.DetailView):
    """
    Generic class-based detail view for a blog.
    """

    model = Dataset

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        dataset = self.get_queryset().first()
        meta_data = dataset.meta_data()
        print(meta_data)
        if meta_data["valid"]:
            for key, value in meta_data.items():
                context[key] = value
        else:
            context[
                "valid"
            ] = "Yout dataset cannot pass validation. It may provide some error in future."

        return context


class DatasetDeleteView(generic.DeleteView):
    model = Dataset
    success_url = reverse_lazy("dataset-list")

    def get_queryset(self):
        id_ = self.kwargs["pk"]
        self.queryset = Dataset.objects.filter(pk=id_)
        return self.queryset

    def get(self, request, *args, **kwargs):
        dataset = self.get_queryset().first()
        if request.user == dataset.owner:
            logger.info(
                "user (%s) want to delete blog dataset (%s)", request.user, dataset
            )
            return super(DatasetDeleteView, self).get(request, *args, **kwargs)
        else:
            logger.info(
                "user (%s) want to delete dataset (%s) by owner (%s)",
                request.user,
                dataset,
                dataset.owner,
            )
            return HttpResponseRedirect(
                reverse("dataset-detail", kwargs={"pk": self.kwargs["pk"]})
            )

    def post(self, request, *args, **kwargs):
        self.items_to_delete = self.request.POST.getlist("itemsToDelete")
        if self.request.POST.get("confirm"):
            logger.info(
                "user (%s) delete dataset (%s)", request.user, self.get_queryset()
            )
            # when confirmation page has been displayed and confirm button pressed
            queryset = self.get_queryset()
            queryset.delete()  # deleting on the queryset is more efficient than on the model object
            return HttpResponseRedirect(self.success_url)
        elif self.request.POST.get("cancel"):
            logger.info(
                "user (%s) not delete dataset (%s)", request.user, self.get_queryset()
            )
            # when confirmation page has been displayed and cancel button pressed
            return HttpResponseRedirect(self.success_url)
        else:
            # when data is coming from the form which lists all items
            return self.get(self, *args, **kwargs)


class DatasetUpdateView(generic.UpdateView):
    model = Dataset
    fields = ["name", "file", "sharing", "code"]
    success_url = reverse_lazy("dataset-list")

    def get_queryset(self):
        id_ = self.kwargs["pk"]
        self.queryset = Dataset.objects.filter(pk=id_)
        return self.queryset

    def get(self, request, *args, **kwargs):
        dataset = self.get_queryset().first()
        if request.user == dataset.owner:
            logger.info("user (%s) want to update dataset (%s)", request.user, dataset)
            return super(DatasetUpdateView, self).get(request, *args, **kwargs)
        else:
            logger.info(
                "user (%s) want to update dataset (%s) by owner (%s)",
                request.user,
                dataset,
                dataset.owner,
            )
            return HttpResponseRedirect(
                reverse("dataset-detail", kwargs={"pk": self.kwargs["pk"]})
            )

    def form_valid(self, form):
        form.instance.date = datetime.today()
        return super().form_valid(form)


class DatasetCreateView(generic.CreateView):
    form_class = DatasetForm
    template_name = "ignis/dataset_form_create.html"
    success_url = reverse_lazy("dataset-list")

    def form_valid(self, form):
        user = self.request.user
        form.instance.owner = user
        form.instance.date = datetime.today()
        return super().form_valid(form)


class NNListView(generic.ListView):
    """
    Generic class-based view for a list of all blogs.
    """

    model = NN
    paginate_by = 15


class NNDetailView(generic.DetailView):
    """
    Generic class-based detail view for a blog.
    """

    model = NN

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        dataset = self.get_queryset().first()
        meta_data = dataset.meta_data()
        context["result"] = meta_data[0].decode("utf-8")
        # print(meta_data)
        # if meta_data["valid"]:
        #     for key, value in meta_data.items():
        #         context[key] = value
        # else:
        #     context[
        #         "valid"
        #     ] = "Yout dataset cannot pass validation. It may provide some error in future."

        return context


class NNDeleteView(generic.DeleteView):
    model = NN
    success_url = reverse_lazy("nn-list")

    def get_queryset(self):
        id_ = self.kwargs["pk"]
        self.queryset = NN.objects.filter(pk=id_)
        return self.queryset

    def get(self, request, *args, **kwargs):
        nn = self.get_queryset().first()
        if request.user == nn.owner:
            logger.info("user (%s) want to delete nn (%s)", request.user, nn)
            return super(NNDeleteView, self).get(request, *args, **kwargs)
        else:
            logger.info(
                "user (%s) want to delete nn (%s) by owner (%s)",
                request.user,
                nn,
                nn.owner,
            )
            return HttpResponseRedirect(
                reverse("nn-detail", kwargs={"pk": self.kwargs["pk"]})
            )

    def post(self, request, *args, **kwargs):
        self.items_to_delete = self.request.POST.getlist("itemsToDelete")
        if self.request.POST.get("confirm"):
            logger.info("user (%s) delete nn (%s)", request.user, self.get_queryset())
            # when confirmation page has been displayed and confirm button pressed
            queryset = self.get_queryset()
            queryset.delete()  # deleting on the queryset is more efficient than on the model object
            return HttpResponseRedirect(self.success_url)
        elif self.request.POST.get("cancel"):
            logger.info(
                "user (%s) not delete nn (%s)", request.user, self.get_queryset()
            )
            # when confirmation page has been displayed and cancel button pressed
            return HttpResponseRedirect(self.success_url)
        else:
            # when data is coming from the form which lists all items
            return self.get(self, *args, **kwargs)


class NNUpdateView(generic.UpdateView):
    model = NN
    fields = ["name", "dataset", "sharing", "code"]
    success_url = reverse_lazy("nn-list")

    def get_queryset(self):
        id_ = self.kwargs["pk"]
        self.queryset = NN.objects.filter(pk=id_)
        return self.queryset

    def get(self, request, *args, **kwargs):
        nn = self.get_queryset().first()
        if request.user == nn.owner:
            logger.info("user (%s) want to update nn (%s)", request.user, nn)
            return super(NNUpdateView, self).get(request, *args, **kwargs)
        else:
            logger.info(
                "user (%s) want to update dataset (%s) by owner (%s)",
                request.user,
                nn,
                nn.owner,
            )
            return HttpResponseRedirect(
                reverse("nn-detail", kwargs={"pk": self.kwargs["pk"]})
            )

    def form_valid(self, form):
        form.instance.date = datetime.today()
        return super().form_valid(form)


class NNCreateView(generic.CreateView):
    form_class = NNForm
    template_name = "ignis/nn_form_create.html"
    success_url = reverse_lazy("nn-list")

    def form_valid(self, form):
        user = self.request.user
        form.instance.owner = user
        form.instance.date = datetime.today()
        return super().form_valid(form)

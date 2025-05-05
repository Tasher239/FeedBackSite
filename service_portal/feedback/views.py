from django.shortcuts import render, redirect
from django.views.generic import DetailView

from .forms import FeedbackForm
from .models import Feedback


def feedback_list(request):
    feedbacks = Feedback.objects.all()
    return render(request, "feedback/list.html", {"feedbacks": feedbacks})


def feedback_new_post(request):
    error = ""
    if request.method == "POST":
        form = FeedbackForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("feedback_list")
        else:
            error = "Форма заполнена некорректно"
    form = FeedbackForm()
    data = {"form": form, "error": error}

    return render(request, "feedback/new_post.html", data)


class FeedbackDetailView(DetailView):
    model = Feedback
    template_name = "feedback/detail_view.html"
    context_object_name = "feedback"

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import QuestionForm
from .models import QAEntry


def home(request):
    return render(request, "home.html")


def register_user(request):

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        if User.objects.filter(username=username).exists():

            return render(
                request,
                "register.html",
                {
                    "error": "Username already exists"
                }
            )

        User.objects.create_user(
            username=username,
            password=password
        )

        return redirect("login")

    return render(request, "register.html")


def login_user(request):
    error = None
    # Respect `next` parameter so users return to protected pages after login
    next_url = request.POST.get('next') or request.GET.get('next') or None

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)
            return redirect(next_url or "home")

        error = "Invalid username or password"

    return render(request, "login.html", {"error": error, "next": next_url})


def logout_user(request):
    logout(request)
    return redirect("login")


@login_required
def ask_question(request):

    if request.method == "POST":

        form = QuestionForm(request.POST)

        if form.is_valid():

            question = form.cleaned_data["question"]

            QAEntry.objects.create(
                user=request.user,
                question_text=question,
                answer_text="Pending",
                plugin_source="Manual"
            )

            return render(
                request,
                "ask_question.html",
                {
                    "form": QuestionForm(),
                    "success": True
                }
            )

    else:
        form = QuestionForm()

    return render(
        request,
        "ask_question.html",
        {
            "form": form
        }
    )


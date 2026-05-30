from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import QuestionForm
from .models import QAEntry
from .groq_service import get_ai_answer


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

    next_url = request.POST.get("next") or request.GET.get("next")

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

    return render(
        request,
        "login.html",
        {
            "error": error,
            "next": next_url
        }
    )


def logout_user(request):
    logout(request)
    return redirect("login")


@login_required
def ask_question(request):

    if request.method == "POST":

        form = QuestionForm(request.POST)

        if form.is_valid():

            question = form.cleaned_data["question"]

            try:
                answer = get_ai_answer(question)

                QAEntry.objects.create(
                    user=request.user,
                    question_text=question,
                    answer_text=answer,
                    plugin_source="Groq"
                )

                return render(
                    request,
                    "ask_question.html",
                    {
                        "form": QuestionForm(),
                        "question": question,
                        "answer": answer,
                        "plugin_source": "Groq",
                        "success": True
                    }
                )

            except Exception as e:
                # On failure, save an explicit error answer and mark plugin_source accordingly
                error_answer = "Unable to generate answer."

                QAEntry.objects.create(
                    user=request.user,
                    question_text=question,
                    answer_text=error_answer,
                    plugin_source="Groq Error"
                )

                return render(
                    request,
                    "ask_question.html",
                    {
                        "form": form,
                        "question": question,
                        "answer": error_answer,
                        "plugin_source": "Groq Error",
                        "error": str(e),
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
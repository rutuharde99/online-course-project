from django.shortcuts import render, redirect
from .models import Question, Choice, Submission


def submit(request):
    if request.method == "POST":
        question_id = request.POST.get("question_id")
        choice_id = request.POST.get("choice_id")

        try:
            question = Question.objects.get(id=question_id)
            choice = Choice.objects.get(
                id=choice_id,
                question=question
            )

            Submission.objects.create(
                question=question,
                selected_choice=choice
            )

            request.session["last_question_id"] = question.id
            request.session["last_choice_id"] = choice.id

            return redirect("show_exam_result")

        except (Question.DoesNotExist, Choice.DoesNotExist, ValueError, TypeError):
            return render(
                request,
                "onlinecourse/submit.html",
                {"error": "Please select a valid choice."}
            )

    return render(request, "onlinecourse/submit.html")


def show_exam_result(request):
    question_id = request.session.get("last_question_id")
    choice_id = request.session.get("last_choice_id")

    if not question_id or not choice_id:
        return redirect("submit")

    try:
        question = Question.objects.get(id=question_id)
        choice = Choice.objects.get(id=choice_id, question=question)

    except (Question.DoesNotExist, Choice.DoesNotExist):
        return redirect("submit")

    return render(
        request,
        "onlinecourse/exam_result.html",
        {
            "question": question,
            "selected_choice": choice,
            "is_correct": choice.is_correct,
        }
    )
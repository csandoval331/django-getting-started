from django.db.models import F
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template import loader
from django.urls import reverse, re_path

from .models import Question
from .models import Choice

# Create your views here.
def index(request):
    # latest_question_list = Question.objects.order_by("-pub_date")[:5]
    # output = " ,  ".join([q.question_text for q in latest_question_list] )
    # return HttpResponse(output)

    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    template = loader.get_template("polls/index.html")
    context = {
        "latest_question_list": latest_question_list,
    }
    return HttpResponse(template.render(context, request) )

def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, "polls/detail.html", {"question": question} )


def result(request, question_id):
    try:
        response = "Youre looking at the results of question %s."
        question = Question.objects.get(pk=question_id)
        #choices = question.
    except:
        raise Http404(" No response on this")
    
    return HttpResponse(response % question_id)

def vote(request, question_id ):
    print("Hello from question_id", question_id)
    
    question = get_object_or_404(Question, pk=question_id )
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"] )
    except (KeyError, Choice.DoesNotExist ):
        # redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didnt select a choice"
            },

        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()

        return HttpResponseRedirect(reverse("polls:result", args=(question.id, )) )
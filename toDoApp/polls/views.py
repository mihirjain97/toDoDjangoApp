from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Question
from django.template import loader
# Create your views here.


def index(request):
    myQuestion = Question
    latestQuestionList = myQuestion.objects.order_by('-pubDate')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latestQuestionList': latestQuestionList
    }
    return HttpResponse(template.render(context, request))


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    response = "You are looking at the results of questions %s. "
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)

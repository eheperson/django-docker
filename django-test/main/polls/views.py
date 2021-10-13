# from django.shortcuts import render
# return HttpResponse(render(context,request))
#
# Create your views here.
#
from django.http import HttpResponse,  HttpResponseRedirect
from django.http.response import Http404
from django.template import context, loader
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
#
from .models import Question, Choice
#
def rawindex(request):
    latest_question_list=Question.objects[:5]
    output = ', '.join([q.question_text for q in latest_question_list])
    return HttpResponse(output)
#
def index(request):
    latest_question_list=Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list' : latest_question_list,
    }
    return HttpResponse(template.render(context,request))
#
def ehe(request):
    return HttpResponse("<h1>ehe</h1>")
#
def info(request):
    return HttpResponse("<h1> that is an information page</h1> <p> information will be here </p>")
#
def detail(request, question_id):
    # get_object_or_404(Question, pk=question_id)
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question':question})
#
# old results function
# def results(request, question_id):
#     response ="You're looking at the result of question %s."
#     return HttpResponse(response % question_id)
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})
#
# old vote function
# def vote(request, question_id):
#     response ="You're voting on question %s."
#     return HttpResponse(response % question_id)
#
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {'question': question, 'error_message': "You didn't select a choice.",})
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


class IndexView(generic.ListView):
    template_name = 'polls/index.html' 
    context_object_name = 'latest_question_list'
    def get_queryset(self):
        """Return the last five published questions.""" 
        return Question.objects.order_by('-pub_date')[:5]
#
class DetailView(generic.DetailView): 
    model = Question
    template_name = 'polls/detail.html'
#
class ResultsView(generic.DetailView): 
    model = Question
    template_name = 'polls/results.html'
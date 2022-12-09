from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Question, Choice
#from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
import json

# Create your views here.

### Generic View (class-based views)
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    """Return the last five published questions."""
    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'



#def index(request):
    ##return HttpResponse("Hello, world. You're at the polls index.")
    #latest_question_list = Question.objects.order_by('-pub_date')[:5]
    ##output = ', '.join([q.question_text for q in latest_question_list])
    ##return HttpResponse(output)
    ##template = loader.get_template('polls/index.html')
    #context = {
    #    'latest_question_list' : latest_question_list,
    #}
    ##return HttpResponse(template.render(context, request))
    #return render(request, 'polls/index.html', context)

#def detail(request,question_id):
    ##return HttpResponse("You're looking at questions %s." % question_id)
    ##try:
        ##question = Question.objects.get(pk=question_id)
    ##except Question.DoesNotExist:
        ##raise Http404("Question does not exist")
    #question = get_object_or_404(Question, pk = question_id)
    #return render(request,'polls/detail.html',{'question':question})

# def results(request,question_id):
#     question = get_object_or_404(Question, pk = question_id)
#     return render(request,'polls/results.html',{'question':question})

# def vote(request,question_id):
#     question = get_object_or_404(Question, pk=question_id)
#
#     # print("[DEBUG_CHOISE]", request.POST['choice'])
#
#     # print("[DEBUG_CHOISE]", request.POST.getlist['choice']) 오류나서 주석처리하심
#
#     for id_check in request.POST.getlist('choice'):
#         try:
#             # selected_choice = question.choice_set.get(pk=request.POST['choice'])
#             selected_choice = question.choice_set.get(pk=id_check)
#         except(KeyError, Choice.DoesNotExist):
#             #Redisplay the question voting form
#             return render(request, 'polls/detail.html', {'question':question, 'error_message':"You didn't select a choice."})
#         else:
#             selected_choice.votes += 1
#             selected_choice.save()
#
#     return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    for id_check in request.POST.getlist('choice'):
        try:
            selected_choice = question.choice_set.get(pk=id_check)
        except(KeyError, Choice.DoesNotExist):
            return render(request, 'polls/detail.html', {'question':question, 'error_message':"You didn't select a choice."})
        else:
            selected_choice.votes += 1
            selected_choice.save()

    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def make_chart_data(data_question):
    my_data = list()
    for choice in data_question.choice_set.all():
        my_dict = dict()
        my_dict['name'] = choice.choice_text
        my_dict['y'] = choice.votes
        my_data.append(my_dict)

    chart_data = [{
        'name': 'Votes',
        'colorByPoint': 'true',
        'data': my_data,
    }]

    return chart_data


def result_chart(request, question_id):
    question=get_object_or_404(Question, pk=question_id)

    chart_data = make_chart_data(question)
    dump = json.dumps(chart_data)

    chart_title = {
        'text': '투표결과 <br>' + question.question_text
    }

    dump_title = json.dumps(chart_title)

    return render(request, 'polls/chart.html', {'chart_data': dump, 'chart_title': dump_title})
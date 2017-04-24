from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.urls import reverse
from .models import Question, Choice


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')
    context = {
        'latest_question_list': latest_question_list
    }
    return render(request, 'index.html', context)


def index_backup(request):
    # 가장 최근의 Question 5개를 가져온다
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # 장고 템플릿 폴더에서 index.html파일을 가져온다
    template = loader.get_template('index.html')
    # 템플릿을 렌더링 할 때 사용할 변수 dictionary
    context = {
        'latest_question_list': latest_question_list
    }
    # Http형식으로 응답을 돌려준다. 내용은 template을 context와 request를 사용해서 렌더링한 결과
    return HttpResponse(template.render(context, request))


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    # return render(request, 'detail.html', {'question': question})
    return render(request, 'detail.html', {'question': question})


def detail_backup(request, question_id):
    # print(request)
    # print(dir(request))
    # meta_dict = request.META
    # for k, v in meta_dict.items():
    #     print('%s : %s' % (k, v))

    # try-except : 예외처리 구문입니다
    # 시도해봅니다!
    try:
        # 전달되어온 question_id가 pk인 Question인스턴스를 가져옵니다
        question = Question.objects.get(pk=question_id)
    # 만약 에러가 발생할경우(근데 DoesNotExist일 경우)
    except Question.DoesNotExist:
        # raise로 에러를 띄워줍니다. 띄워줄 에러는 Http404
        raise Http404('Question does not exist')
    # 발생하지 않으면 except구문이 실행되지않고, detail.html을 render해서 보여줍니다
    return render(request, 'detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'results.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    print(request.POST)
    try:
        choice_id = request.POST['choice']
        # print('choice_id : %s' % choice_id)
        selected_choice = question.choice_set.get(pk=choice_id)

        # selected_choice = get_object_or_404(Choice, pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'detail.html', {
            'question': question,
            'error_message': 'You didn\'t select a choice',
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        redirect_url = reverse('polls:results', args=(question.id,))
        # redirect_url = reverse('polls:detail', args=(question.id,))
        print('redirect_url : %s' % redirect_url)
        # redirect_url = '/polls/%s/results/' % question.id
        return HttpResponseRedirect(redirect_url)


def add_choice(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    print(request.POST)
    try:
        choice_name = request.POST['choice_name']
        print('choice_name : %s' % choice_name)

        if Choice.objects.filter(question=question, choice_text__iexact=choice_name).exists():
            return HttpResponse('Choice [%s] is exist' % choice_name)
        elif choice_name == '':
            return HttpResponse('choice_name is required')
        elif len(choice_name) < 3:
            return HttpResponse('choice_name is too short')
    except KeyError:
        return HttpResponse('choice_name key does not exist')

    choice = question.choice_set.create(choice_text=choice_name)
    print('created choice : %s' % choice)
    # choice = Choice(question=question, choice_text=choice_name)
    # choice.save()

    redirect_url = reverse('polls:detail', args=(question_id,))
    # /polls/{{ question.id }}/
    # redirect_url = 'http://naver.com'
    return HttpResponseRedirect(redirect_url)
    # return render(request, 'detail.html', {'question': question})
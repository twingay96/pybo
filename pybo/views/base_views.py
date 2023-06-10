from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count
from pybo.models import Answer, Category, Question




def index(request, category_name='qna'):
    '''
    pybo list 목록 출력
    '''
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw','')   # 검색어
    so = request.GET.get('so', 'recent')  # 정렬기준

    category_list = Category.objects.all()
    category = get_object_or_404(Category, name=category_name)
    question_list = Question.objects.filter(category=category)

    if so == 'recommend':

        # annotate()는 필드 하나를 만들고 거기에 '어떤 내용'을 채우게 만드는 것이다.
        # 엑셀에서 컬럼 하나를 만드는 것과 같다고 보면 된다. 내용에는
        # 1. 다른 필드의 값을 그대로 복사하거나, 2. 다른 필드의 값들을 조합한 값을 넣을 수 있다.
        question_list =question_list.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
        # Count('voter')는 voter의 개수가 담기는 새로운 필드를 만든다음 그 필드를 num_voter라고 명명한다.
        # order_by('-num_voter', '-create_date') : annotate에서 정의한 num_voter을 기준으로 정렬한다.
    elif so == 'popular':
        question_list = question_list.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:  # so == 'recent':
        question_list = question_list.order_by('-create_date')

    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw) |  # 내용 검색
            Q(answer__content__icontains=kw) |  # 답변 내용 검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이 검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이 검색
        ).distinct()
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj, 'page': page, 'kw': kw, 'category_list': category_list, 'category': category ,
               'so': so }
    return render(request, 'pybo/question_list.html', context)




def detail(request,question_id):
    page = request.GET.get('page', '1')  # 페이지
    so = request.GET.get('so', 'recommend')  # 정렬기준

    question = get_object_or_404(Question, pk=question_id)
    # 요청한 question_id에 있는 답변들 필터링해서 answer_list로 명명
    answer_list = Answer.objects.filter(question=question)

    # 페이징처리
    paginator = Paginator(answer_list, 5)  # 페이지당 5개식 보여주기
    page_obj = paginator.get_page(page)

    context = {'question': question, 'answer_list': page_obj, 'page': page, 'so': so, 'category': question.category}
    return render(request, 'pybo/question_detail.html', context)


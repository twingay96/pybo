from django.db import models
from django.db.models import Count
from django.urls import reverse
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    has_answer = models.BooleanField(default=True)  # 답변가능 여부

    def __str__(self):
    #     return self.name
        return self.description

    def get_absolute_url(self):
        return reverse('pybo:index', args=[self.name])


class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_question')  # 추천인 추가
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_question')
    seen_cnt = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.subject
    '''
    @staticmethod
    def order_by_so(question_list, so):
        if so == 'recommend':
            
            # annotate()는 필드 하나를 만들고 거기에 '어떤 내용'을 채우게 만드는 것이다. 
            # 엑셀에서 컬럼 하나를 만드는 것과 같다고 보면 된다. 내용에는 
            # 1. 다른 필드의 값을 그대로 복사하거나, 2. 다른 필드의 값들을 조합한 값을 넣을 수 있다.
            
            question_list = question_list.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
            # Count('voter')는 voter의 개수가 담기는 새로운 필드를 만든다음 그 필드를 num_voter라고 명명한다.
            # order_by('-num_voter', '-create_date') : annotate에서 정의한 num_voter을 기준으로 정렬한다.
        elif so == 'popular':
            question_list = question_list.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
        else:  # so == 'recent':
            question_list = question_list.order_by('-create_date')

        return question_list
    '''

    def get_absolute_url(self):
        return reverse('pybo:detail', args=[self.id])
    # 조회수 기능 추가
    @property
    def update_counter(self):
        self.seen_cnt = self.seen_cnt+1
        self.save()
        # return self.seen_cnt
    # https://integer-ji.tistory.com/247


class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_answer')  # 추천인 추가

    def __str__(self):
        return self.content

    @staticmethod
    def order_by_so(answer_list, so):
        # 정렬
        if so == 'recommend':

            answer_list = answer_list.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
        else:  # so == 'recent':
            answer_list = answer_list.order_by('-create_date')

        return answer_list

    def get_page(self, so='recommend'):
        # https://stackoverflow.com/questions/1042596/get-the-index-of-an-element-in-a-queryset
        answer_list = Answer.order_by_so(self.question.answer_set.all(), so)

        index = 0
        for _answer in answer_list:
            index += 1
            if self == _answer:
                break

        return (index - 1)//5 + 1

    # def get_relative_url(self, so, page):
    #     return reverse('pybo:detail', args=[self.question.id]) + f'?page={page}&so={so}#answer_{self.id}'

    def get_absolute_url(self):
        return reverse('pybo:detail', args=[self.question.id]) + f'?page={self.get_page()}#answer_{self.id}'


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_comment')
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        if self.question:
            return reverse('pybo:detail', args=[self.question.id]) + '#comment_question_start'
        else:  # if self.answer:
            return reverse('pybo:detail', args=[self.answer.question.id]) + \
                   f'?page={self.answer.get_page()}#comment_{self.id}'  # todo comment_id 가능?
from django.core.exceptions import ValidationError
from django.db import models
from django_extensions.db.models import TimeStampedModel

from apps.members.models import User

__all__ = (
    'Poll',
    'Choice',
    'Vote',
)


class Poll(TimeStampedModel):
    is_multiple = models.BooleanField('복수항목 투표가능', default=False)
    allow_anonymous = models.BooleanField('익명', default=False)

    name = models.CharField('설문조사명', max_length=100)
    author = models.ForeignKey(
        User, verbose_name='작성자', on_delete=models.SET_NULL,
        related_name='poll_set_by_author', blank=True, null=True)
    participants = models.ManyToManyField(
        User, verbose_name='참여자들',
        related_name='poll_set_by_participants', blank=True)

    _order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = '설문조사'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ('_order',)

    def __str__(self):
        return self.name


class Choice(TimeStampedModel):
    is_text = models.BooleanField('주관식', default=False)
    poll = models.ForeignKey(Poll, verbose_name='설문조사', on_delete=models.CASCADE)
    name = models.CharField('선택지', max_length=50)

    _order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = '선택지'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ('_order',)

    def __str__(self):
        return f'{self.poll.name} | {self.name}'


class Vote(TimeStampedModel):
    choice = models.ForeignKey(Choice, verbose_name='선택지', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='투표자', on_delete=models.CASCADE)
    text = models.CharField('주관식 응답', max_length=100, blank=True)

    class Meta:
        verbose_name = '투표'
        verbose_name_plural = f'{verbose_name} 목록'
        constraints = [
            models.UniqueConstraint(fields=['choice', 'user'], name='unique_user_choice'),
        ]

    def __str__(self):
        return f'{self.choice.poll.name} | {self.choice.name} ({self.user.name})'

    def save(self, **kwargs):
        # 새로생성되며, 선택지의 설문조사가 복수응답을 허용하지 않는 경우
        if not self.pk and not self.choice.poll.is_multiple:
            # 설문조사의 선택지들 중, 투표한 사용자가 현재 투표의 사용자에 해당하는 투표객체가 존재하는 경우 예외
            if self.choice.poll.choice_set.filter(vote__user=self.user).exists():
                raise ValidationError('복수선택지 허용되지 않은 경우, 1개의 투표만 가능합니다')

        if self.choice.is_text and not self.text:
            raise ValidationError('주관식 응답의 경우, 항목을 입력하셔야 합니다')
        super().save(**kwargs)

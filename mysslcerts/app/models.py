from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Tag(models.Model):
    word = models.CharField(max_length=35, unique=True)
    created = models.DateTimeField('Created', auto_now_add=True)
    modified = models.DateTimeField('Modified', auto_now=True)

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")
        ordering = ['word']

    def __unicode__(self):
        return u'%s' % (self.word)

class Topic(models.Model):
    name = models.CharField(max_length=200, unique=True)
    sort_order = models.IntegerField(_('sort order'), default=0,
                    help_text=_('The order you would like the topic to be displayed.'))
    related_questions = models.ManyToManyField('Question', related_name="related_questions", blank=True)
    created = models.DateTimeField('Created', auto_now_add=True)
    modified = models.DateTimeField('Modified', auto_now=True)

    class Meta:
        verbose_name = _("Topic")
        verbose_name_plural = _("Topics")
        ordering = ['sort_order', 'name']

    def __unicode__(self):
        return u'%s' % (self.name)

class Question(models.Model):
    enabled = models.BooleanField('Enabled?', default=True)
    text = models.CharField(max_length=200, unique=True, help_text=_('What is the question?'))
    answer = models.CharField(max_length=50000, blank=True, help_text=_('Enter the answer.'))
    sort_order = models.IntegerField(_('sort order'), default=0, help_text=_('The order you would like the question to be displayed.'))
    topic = models.ForeignKey('Topic', related_name="related_topic", default='', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name="related_tags", default='')

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")
        ordering = ['sort_order', 'text']

    def __unicode__(self):
        return u'%s' % (self.text)


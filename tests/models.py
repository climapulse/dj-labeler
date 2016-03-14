# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division, absolute_import
from django.contrib.auth.models import User
from django.db import models
from labeler import ModelTranslations


i18n_issue_type = ModelTranslations(
    labels=dict(
        key='label:Key',
        label='label:Label'
    ),
    help_texts=dict(
        key='Technical key',
        label='Human-friendly label'
    ),
    error_messages=dict(
        key=dict(
            unique='Key must be unique'
        )
    ),
    name='Type',
    name_plural='Types',
    errors=dict(
        no_profanity='Please do not use profanity'
    ),
    messages=dict(
        thankyou='Thank you for reporting this issue'
    )
)


i18n_state = ModelTranslations(
    labels=dict(
        key='state:Key',
        label='state:Label',
        end_state='state:End state'
    ),
    help_texts=dict(
        key='A technical key',
        label='A human-friendly label',
        end_state='Whether this state is and end state or not'
    ),
    name='Issue state',
    name_plural='Issue states'
)


i18n_issue = ModelTranslations(
    labels=dict(
        issue_type='Type of issue',
        title='Title',
        description='A short description',
        priority='Priority of this issue',
        state='The state of the issue',
        reporter='Who reported it'
    ),
    help_texts=dict(
        issue_type='Just pick something',
        description='Be as descriptive as possible',
        priority='The priority will be evaluated later on. Everybody thinks their issue is most important.',
    ),
    priorities={
        0: 'Trivial',
        2: 'Low',
        5: 'Medium',
        7: 'High',
        10: 'Catastrophical'
    }
)

i18n_comment = ModelTranslations(
    labels=dict(
        issue='The issue this comment relates to',
        content='Comment',
        created='When was the comment added'
    ),
    help_texts=dict(
        content='No profanity please'
    ),
    name='Comment',
    name_plural='Comments'
)


@i18n_issue_type.inject
class IssueType(models.Model):
    key = models.SlugField(max_length=10, unique=True)
    label = models.CharField(max_length=100)


@i18n_state.inject
class State(models.Model):
    key = models.SlugField(max_length=30)
    label = models.CharField(max_length=100)
    end_state = models.BooleanField(default=False)


PRIORITIES = [(i, i18n_issue['priorities'][i]) for i in [0, 2, 5, 7, 10]]


@i18n_issue.inject
class Issue(models.Model):
    issue_type = models.ForeignKey(IssueType, related_name='issues')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    priority = models.PositiveIntegerField(choices=PRIORITIES)
    state = models.ForeignKey(State, related_name='issues')
    reporter = models.ForeignKey(User, related_name='reported_issues')


@i18n_comment.inject
class Comment(models.Model):
    issue = models.ForeignKey(Issue, related_name='comments')
    content = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    commenter = models.ForeignKey(User, related_name='comments')

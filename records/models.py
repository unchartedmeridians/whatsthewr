from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Game(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    game = models.ForeignKey(Game)
    tab_index = models.IntegerField()

    def __unicode__(self):
        return self.name

class Record(models.Model):
    game = models.ForeignKey(Game, null=True, blank=True)
    game_as_text = models.CharField(max_length=100)
    category = models.ForeignKey(Category, null=True, blank=True)
    category_as_text = models.CharField(max_length=100)
    runner = models.CharField(max_length=100)
    time = models.TimeField()
    link = models.URLField()
    approved = models.BooleanField(default=False)
    date_submitted = models.DateTimeField(default=timezone.now())
    date_approved = models.DateTimeField(null=True, blank=True)
    submitted_by = models.ForeignKey(User, editable=False,
                                     related_name='record_submitted_by')
    submitted_by_ip = models.GenericIPAddressField(editable=False)
    approved_by = models.ForeignKey(User, null=True,
                                    blank=True, editable=False,
                                    related_name='record_approved_by')

    def __unicode__(self):
        if self.approved:
            return "{0} ({1}) by {2} in {3}".format(self.game, self.category, 
                                                    self.runner, self.time)
        else:
            return  "{0} ({1}) by {2} in {3}".format(self.game_as_text, 
                                                     self.category_as_text, 
                                                     self.runner, self.time)
    class Meta:
        permissions = (
            ('can_approve', 'Can approve pending records'),
        )

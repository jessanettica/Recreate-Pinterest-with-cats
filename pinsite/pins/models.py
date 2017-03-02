import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.http import HttpResponse

from pinsite import settings
import json


class User(AbstractUser):
    full_name = models.CharField(max_length=100, blank=True)

    pin_user_id = models.PositiveIntegerField(null=True, blank=True)

    img_url = models.CharField(max_length=255, default="", blank=True)


class Board(models.Model):
    """A model that contains data for a single board."""
    # creator of the board, when deleted related objects are also deleted
    owner_id = models.PositiveIntegerField(null=True, blank=True)

    name = models.CharField(max_length=255, default="", blank=True)

    url = models.CharField(max_length=255, default="", blank=True)


class Pin(models.Model):
    """A model that contains data for a single pin."""
    # when deleted related objects are also deleted
    pinner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    boards = models.ManyToManyField(Board, related_name='pins', blank=True)

    title = models.CharField(max_length=255, default="", blank=True)
    # used to determine which pins to reuse as the user scrolls
    is_used = models.BooleanField(default=False, blank=True)

    provider_name = models.CharField(max_length=255, default="", blank=True)

    buyable_product = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=datetime.datetime.now)

    description = models.TextField(default="", blank=True)

    pinterest_id = models.PositiveIntegerField(null=True, blank=True)

    img_url = models.CharField(max_length=255, default="", blank=True)

    img_height = models.PositiveIntegerField(default=236, null=True, blank=True)

    like_count = models.PositiveIntegerField(default=0, null=True, blank=True)

    repin_count = models.PositiveIntegerField(default=0, null=True, blank=True)

    def as_dict(self):
        """Return dictionary representation of object."""
        return {
            "pinterest_id": self.pinterest_id,
            "pinner": {
                "username": self.pinner.username,
                "full_name": self.pinner.full_name,
                "img_url": self.pinner.img_url
            },
            "boards": {
                "name": self.boards.first().name,
                "url": self.boards.first().url,
                "owner_id": self.boards.first().owner_id
                },
            "title": self.title,
            "is_used": self.is_used,
            "buyable_product": self.buyable_product,
            "created_at": self.created_at,
            "description": self.description,
            "img_url": self.img_url,
            "img_height": self.img_height,
            "like_count": self.like_count,
            "repin_count": self.repin_count
        }

from django.conf import settings
from django.test import TestCase
# Импортируем функцию reverse(), она понадобится для получения адреса страницы.
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

from datetime import datetime, timedelta

from notes.models import Note
from notes.forms import NoteForm


User = get_user_model()

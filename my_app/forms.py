from django.forms import ModelForm
from .models import CommentPost

class CommentForm(ModelForm):
	"""Koment formalarini chaqirish"""
	class Meta:
		model = CommentPost
		fields = ('text', 'user', 'post')
		
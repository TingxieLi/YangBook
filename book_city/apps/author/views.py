from django.shortcuts import render, reverse, redirect
from django.views import View
from .models import Author
from operation.models import Attention


class AuthorDetailView(View):
    @staticmethod
    def get(request, author_id):
        try:
            author = Author.objects.get(id=author_id)
        except Author.DoesNotExist:
            return redirect(reverse('index'))
        if not request.user.is_authenticated or not Attention.objects.filter(attention_man=request.user, attention_author=author):
            author_status = False
        else:
            author_status = True
        context = {
            'author': author,
            'author_status': author_status
        }
        return render(request, 'author.html', context)

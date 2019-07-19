from django.shortcuts import render
from django.views import View
from user.models import Member
from book.models import Book, Chapter
from author.models import Author
from .models import Collect, Attention, Comment, Recommend, BookmarkModel
from django.db.models import Q
from django.http import JsonResponse
from django_redis import get_redis_connection


class SearchView(View):
    @staticmethod
    def get(request):
        search_key = request.GET.get('search_key')
        if not search_key:
            book_list = ''
        else:
            book_list = Book.objects.filter(Q(title__contains=search_key) | Q(author__name__contains=search_key))
        return render(request, 'search.html', {'book_list': book_list})


class CollectView(View):
    @staticmethod
    def post(request):
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'fail', 'msg': '请你先登录'})
        book_id = request.POST.get('book_id')
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return JsonResponse({'status': 'fail', 'msg': '书本信息错误'})
        collect = Collect.objects.filter(collect_book=book, collect_man=request.user)
        if collect:
            collect.delete()
            book.collect_num -= 1
            book.save()
            return JsonResponse({'status': 'ok', 'msg': '移出书架成功'})
        else:
            Collect.objects.create(collect_book=book, collect_man=request.user)
            book.collect_num += 1
            book.save()
            return JsonResponse({'status': 'ok', 'msg': '加入书架成功'})


class AttentionView(View):
    @staticmethod
    def post(request):
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'fail', 'msg': '请你先登录'})
        author_id = request.POST.get('author_id')
        try:
            author = Author.objects.get(id=author_id)
        except Author.DoesNotExist:
            return JsonResponse({'status': 'fail', 'msg': '作者信息错误'})
        attention = Attention.objects.filter(attention_author=author, attention_man=request.user)
        if attention:
            attention.delete()
            author.attention_num -= 1
            author.save()
            return JsonResponse({'status': 'ok', 'msg': '取消关注成功'})
        else:
            Attention.objects.create(attention_author=author, attention_man=request.user)
            author.attention_num += 1
            author.save()
            return JsonResponse({'status': 'ok', 'msg': '关注成功'})


class DeleteHistoryView(View):
    @staticmethod
    def post(request):
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'fail', 'msg': '请你先登录'})
        book_id = request.POST.get('book_id', '')
        conn = get_redis_connection('default')
        history_key = 'history_{}'.format(request.user.id)
        book_id_list = conn.lrange(history_key, 0, -1)
        if book_id.encode() in book_id_list:
            conn.lrem(history_key, 0, book_id)
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'fail', 'msg': '书本信息错误'})


class RecommendView(View):
    @staticmethod
    def post(request):
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'fail', 'msg': '请你先登录'})
        member = Member.filter_member(request.user)
        if not member:
            return JsonResponse({'status': 'fail', 'msg': '你不是会员'})
        if member.ticket_num <= 0:
            return JsonResponse({'status': 'fail', 'msg': '推荐票数量不足'})
        book_id = request.POST.get('book_id')
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return JsonResponse({'status': 'fail', 'msg': '书本信息错误'})

        recommend = Recommend.objects.filter(recommend_book=book, recommend_man=request.user)
        if recommend:
            recommend = recommend[0]
            recommend.recommend_num += 1
            recommend.save()
        else:
            Recommend.objects.create(recommend_man=request.user, recommend_book=book)
        book.recommend_num += 1
        book.save()
        member.ticket_num -= 1
        member.save()
        return JsonResponse({'status': 'ok', 'msg': '推荐成功'})


class CommentView(View):
    @staticmethod
    def post(request):
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'fail', 'msg': '请你先登录'})
        book_id = request.POST.get('book_id')
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return JsonResponse({'status': 'fail', 'msg': '书本信息错误'})
        comment_content = request.POST.get('comment_content')
        if 0 < len(comment_content) <= 300:
            Comment.objects.create(comment_book=book, comment_man=request.user, comment_content=comment_content)
            return JsonResponse({'status': 'ok', 'msg': '评论成功'})
        else:
            return JsonResponse({'status': 'fail', 'msg': '评论内容不能为空，且在300字以内'})


class BookmarkView(View):
    @staticmethod
    def post(request):
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'fail', 'msg': '请你先登录'})
        chapter_id = request.POST.get('chapter_id')
        try:
            chapter = Chapter.objects.get(id=chapter_id)
        except Chapter.DoesNotExist:
            return JsonResponse({'status': 'fail', 'msg': '章节信息错误'})
        bookmark = BookmarkModel.objects.filter(mark_user=request.user, mark_book=chapter.book)
        if bookmark:
            bookmark = bookmark[0]
            if bookmark.mark_chapter == chapter:
                bookmark.delete()
                return JsonResponse({'status': 'ok', 'msg': '书签删除成功'})
            bookmark.mark_chapter = chapter
            bookmark.save()
        else:
            BookmarkModel.objects.create(mark_user=request.user, mark_book=chapter.book, mark_chapter=chapter)
        return JsonResponse({'status': 'ok', 'msg': '书签添加成功'})


class DownloadView(View):
    @staticmethod
    def post(request):
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'fail', 'msg': '你未登录'})
        if not Member.filter_member(request.user):
            return JsonResponse({'status': 'fail', 'msg': '你不是会员'})
        book_id = request.POST.get('book_id')
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return JsonResponse({'status': 'fail', 'msg': '书本信息错误'})
        download_url = book.download_url
        return JsonResponse({'status': 'ok', 'download_url': download_url})

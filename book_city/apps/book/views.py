from django.shortcuts import render, reverse, redirect
from django.views import View
from .models import Banner, Book, Chapter
from trade.models import MemberDuration
from operation.models import Collect, Comment, BookmarkModel
from django.core.paginator import Paginator, EmptyPage
from django.core.exceptions import FieldError
from django_redis import get_redis_connection


def member_context(request):
    member_durations = MemberDuration.objects.all()
    return {'member_durations': member_durations}


class IndexView(View):
    @staticmethod
    def get(request):
        banner_list = Banner.objects.all().order_by('-create_time')[:4]
        wx_books = Book.objects.filter(type='wx').order_by('-collect_num')[:8]
        xh_books = Book.objects.filter(type='xh').order_by('-collect_num')[:8]
        ds_books = Book.objects.filter(type='ds').order_by('-collect_num')[:8]
        kb_books = Book.objects.filter(type='kb').order_by('-collect_num')[:8]
        hot_books = Book.objects.all().order_by('-click_num')[:6]
        new_books = Book.objects.all().order_by('-create_time')[:6]

        context = {
            'banner_list': banner_list,
            'wx_books': wx_books,
            'xh_books': xh_books,
            'ds_books': ds_books,
            'kb_books': kb_books,
            'hot_books': hot_books,
            'new_books': new_books,
            'title': 'index'
        }
        return render(request, 'index.html', context)


class TypeView(View):
    @staticmethod
    def get(request, category, page_num):
        book_list = Book.objects.filter(type=category)
        if not book_list:
            return redirect(reverse('book:type', args=('wx', 1)))

        sort = request.GET.get('sort')
        if sort:
            book_list = book_list.order_by('-' + sort)

        pa = Paginator(book_list, 10)
        try:
            book_page = pa.page(page_num)
        except EmptyPage:
            book_page = pa.page(pa.num_pages)
        num_pages = pa.num_pages
        if num_pages <= 5:
            pages = range(1, num_pages + 1)
        elif page_num <= 3:
            pages = range(1, 6)
        elif num_pages - page_num <= 2:
            pages = range(num_pages - 4, num_pages + 1)
        else:
            pages = range(page_num - 2, page_num + 3)
        context = {
            'category': category,
            'book_page': book_page,
            'pages': pages,
            'sort': sort,
            'title': 'type'
        }
        return render(request, 'type.html', context)


class RankView(View):
    @staticmethod
    def get(request, sort, page_num):
        status = request.GET.get('status')
        if status:
            try:
                book_list = Book.objects.filter(status=status).order_by('-' + sort)[:100]
            except FieldError:
                return redirect(reverse('book:rank', args=('click_num', 1)))
        else:
            book_list = Book.objects.all().order_by('-' + sort)[:100]

        pa = Paginator(book_list, 10)
        try:
            book_page = pa.page(page_num)
        except EmptyPage:
            book_page = pa.page(pa.num_pages)
        num_pages = pa.num_pages
        if num_pages <= 5:
            pages = range(1, num_pages + 1)
        elif page_num <= 3:
            pages = range(1, 6)
        elif num_pages - page_num <= 2:
            pages = range(num_pages - 4, num_pages + 1)
        else:
            pages = range(page_num - 2, page_num + 3)
        context = {
            'book_page': book_page,
            'pages': pages,
            'sort': sort,
            'status': status,
            'title': 'rank'
        }
        return render(request, 'rank.html', context)


class DetailView(View):
    @staticmethod
    def get(request, book_id):
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return redirect(reverse('index'))
        if not request.user.is_authenticated or not Collect.objects.filter(collect_man=request.user, collect_book=book):
            collect_status = False
        else:
            collect_status = True
        recommend_book_list = Book.objects.filter(type=book.type).order_by('-recommend_num')[:8]
        author_book_list = book.author.book_set.all().exclude(id=book_id)[:3]
        book.click_num += 1
        book.save()

        comment_list = Comment.objects.filter(comment_book=book)
        chapter = Chapter.objects.get(sort_number=0, book=book)
        if request.user.is_authenticated:
            conn = get_redis_connection('default')
            history_key = 'history_{}'.format(request.user.id)
            book_id_list = conn.lrange(history_key, 0, -1)
            book_id = str(book_id)
            if book_id.encode() in book_id_list:
                conn.lrem(history_key, 0, book_id)
            conn.lpush(history_key, book_id)

            bookmark = BookmarkModel.objects.filter(mark_book=book, mark_user=request.user)
            if bookmark:
                chapter = bookmark[0].mark_chapter

        chapter_id = chapter.id

        context = {
            'book': book,
            'chapter_id': chapter_id,
            'collect_status': collect_status,
            'author_book_list': author_book_list,
            'recommend_book_list': recommend_book_list,
            'comment_list': comment_list
        }
        return render(request, 'detail.html', context)


class ChapterView(View):
    @staticmethod
    def get(request, book_id):
        chapter_list = Chapter.objects.filter(book__id=book_id)
        if not chapter_list:
            return redirect(reverse('index'))

        context = {
            'chapter_list': chapter_list,
        }
        return render(request, 'chapter.html', context)


class ContentView(View):
    @staticmethod
    def get(request, chapter_id):
        try:
            chapter = Chapter.objects.get(id=chapter_id)
        except Chapter.DoesNotExist:
            return redirect(reverse('index'))

        try:
            precious_chapter = Chapter.objects.get(sort_number=chapter.sort_number - 1, book=chapter.book)
        except Chapter.DoesNotExist:
            precious_chapter = None

        try:
            next_chapter = Chapter.objects.get(sort_number=chapter.sort_number + 1, book=chapter.book)
        except Chapter.DoesNotExist:
            next_chapter = None

        context = {
            'chapter': chapter,
            'precious_chapter': precious_chapter,
            'next_chapter': next_chapter
        }
        return render(request, 'content.html', context)

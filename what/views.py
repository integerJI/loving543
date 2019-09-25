from django.shortcuts import render, redirect, get_object_or_404, reverse
from .forms import PostForm
from django.contrib import messages
from .models import Memos, Comment, Tag, Tag2
from who.models import Profile
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect
try:
    from django.utils import simplejson as json
except ImportError:
    import json
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.urls import reverse_lazy
from django.db.models import Q

def index(request, tag=None, tag2=None):
    sort = request.GET.get('sort','')
    if sort == 'likes':
        memo = Memos.objects.prefetch_related('tag_set').select_related('name__profile').annotate(like_count=Count('likes')).filter(secret = False).order_by('-like_count', '-update_date')
        return render(request, 'index.html', {'memo' : memo})
    elif sort == 'mypost':
        user = request.user
        memo = Memos.objects.prefetch_related('tag_set').select_related('name__profile').filter(name = user, secret = False).order_by('-update_date')
        return render(request, 'index.html', {'memo' : memo})
    elif sort == 'mylike':
        user = request.user
        memo = Memos.objects.prefetch_related('tag_set').select_related('name__profile').filter(likes=user, secret = False).order_by('-update_date')
        return render(request, 'index.html', {'memo' : memo})
    elif sort == 'secret':
        user = request.user
        memo = Memos.objects.prefetch_related('tag_set').select_related('name__profile').filter(secret = True, name = user).order_by('-update_date')
        return render(request, 'index.html', {'memo' : memo})
    else:

        if tag:
            memo = Memos.objects.filter(tag_set__tag_name__iexact=tag).prefetch_related('tag_set').select_related('name__profile')
            
        elif tag2:
            memo = Memos.objects.filter(tag_set2__tag_name2__iexact=tag2).prefetch_related('tag_set2').select_related('name__profile')

        else:
            memo = Memos.objects.all().prefetch_related('tag_set','tag_set2').select_related('name__profile').order_by('-update_date')

        return render(request, 'index.html', {'tag': tag,'tag2': tag2,'memo': memo})




        

def post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        
        if form.is_valid(): 
            post = form.save(commit = False)
            post.name = User.objects.get(username = request.user.get_username())
            post.generate()
            post.tag_save()
            post.tag_save2()
            post.save()
            return redirect('index')
    else:
        form = PostForm() 
        return render(request, 'post.html', {'form' : form})  

def detail(request, memo_id):
    memo = get_object_or_404(Memos, pk=memo_id)
    return render(request, 'detail.html', {'memo': memo})

def modify(request, memokey):
    if request.method == "POST":
        memo = Memos.objects.get(pk = memokey)
        form = PostForm(request.POST, request.FILES, instance=memo)

        if form.is_valid():
            memo = form.save(commit=False)
            memo.save()

            context = {'memo': memo,}
            content = request.POST.get('content')
            
            messages.info(request, '수정 완료')
            return render(request, 'detail.html', context=context)

    else:
        memo = Memos.objects.get(pk = memokey)
        if memo.name == User.objects.get(username = request.user.get_username()):
            memo = Memos.objects.get(pk = memokey)
            form = PostForm(instance = memo)
            
            return render(request, 'modify.html', {'memo' : memo, 'form' : form})
        else:
            return render(request, 'warning.html')

def delete(request, memokey):
    memo = Memos.objects.get(pk = memokey)
    if memo.name == User.objects.get(username = request.user.get_username()):
        memo.delete()
        return redirect('index')
    else:
        return render(request, 'warning.html')


@login_required
@require_POST
def like(request):
    if request.method == 'POST':
        user = request.user 
        memo_id = request.POST.get('pk', None)
        memo = Memos.objects.get(pk = memo_id)

        if memo.likes.filter(id = user.id).exists():
            memo.likes.remove(user) 
            message = '좋아요 취소'
        else:
            memo.likes.add(user)
            message = '좋아요!'

    context = {'likes_count' : memo.total_likes, 'message' : message}
    return HttpResponse(json.dumps(context), content_type='application/json')


@login_required
def comment_write(request, memokey):
    if request.method =='POST':
        post = get_object_or_404(Memos, pk=memokey)

        context = {'post': post,}
        content = request.POST.get('content')

        conn_user = request.user
        conn_profile = Profile.objects.get(user=conn_user)

        if not content:
            messages.info(request, '댓글을 입력해 주세요')
            return redirect('detail', memokey)

        Comment.objects.create(post=post, comment_writer=conn_profile, comment_contents=content)
        return redirect('detail', memokey)

@login_required
def comment_delete(request, memo_pk, pk):
    post = get_object_or_404(Memos, pk=memo_pk)
    comment = get_object_or_404(Comment, pk=pk)
        
    context = {'post': post,}
    content = request.POST.get('content')

    conn_user = request.user
    conn_profile = Profile.objects.get(user=conn_user)


    if conn_profile == comment.comment_writer:
        comment.delete()
        return redirect('detail', memo_pk)
    else:
        return render(request, 'warning.html')

def search(request):
    memo = Memos.objects.all()
    q = request.GET.get('q', False) 

    if q:
        memo = memo.filter(Q(text__icontains=q) | Q(text3__icontains=q) | Q(text2__icontains=q))
        return render(request, 'search.html', {'memo' : memo, 'q' : q})

    else:
        messages.info(request, '입력된 값이 없습니다.')
        return redirect('index')

def multisearch(request):
    memo = Memos.objects.all()
    p = request.GET.get('p', False) 

    if p:
        memo = memo.filter(Q(text__icontains=p) | Q(text3__icontains=p) | Q(text2__icontains=p))
        return render(request, 'search.html', {'memo' : memo, 'p' : p})

    else:
        messages.info(request, '입력된 값이 없습니다.')
        return redirect('index')
        


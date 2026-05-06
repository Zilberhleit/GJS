from allauth.account.views import SignupView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from jams.models.comment import Comment

from users.forms import CommentForm, PostForm
from users.models import Post, Team


@login_required
def create_post(request, team_id=None):
    """Представление создания поста"""
    form = PostForm()

    team = None
    if team_id:
        team = get_object_or_404(Team, id=team_id)
        if request.user not in team.members.all():
            return redirect("team_detail", team_id=team.id)

    if request.method == "POST":
        form = PostForm(request.POST, request._files)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user

            if team:
                post.team = team

            post.save()
            if team:
                return redirect("team_detail", id=team.id)
            else:
                return redirect("profile_detail", username=request.user.username)
    else:
        form = PostForm()
    return render(
        request,
        template_name="pages/user_pages/create_post.html",
        context={"form": form},
    )


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        messages.error(request, "У вас нет прав редактировать этот пост")
        if post.team:
            return redirect("team_detail", id=post.team.id)
        return redirect("post_detail", id=post.id)

    if request.method == "POST":
        form = PostForm(request.POST, request._files, instance=post)
        if form.is_valid():
            form.save()
            if post.team:
                return redirect("team_detail", id=post.team.id)
            return redirect("profile_detail", username=post.author.username)
        else:
            messages.error(request, "Ошибки в форме")
    else:
        form = PostForm(instance=post)

    return render(
        request,
        template_name="pages/user_pages/create_post.html",
        context={
            "form": form,
            "post": post,
            "is_edit": True,
        },
    )


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        messages.error(request, "Нельзя удалить не свой пост")
        return HttpResponseForbidden("У вас нет прав на удаление этого поста")

    username = post.author.username

    post.delete()

    return redirect("profile_detail", username=username)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.post.all()
    form = CommentForm()
    return render(
        request,
        template_name="pages/user_pages/post_detail.html",
        context={"post": post, "comments": comments, "form": form},
    )


def posts_page(request):
    posts = list(Post.objects.all())
    return render(
        request, template_name="pages/user_pages/posts.html", context={"posts": posts}
    )


@login_required
def add_comment_to_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post_id = post
            comment.save()
            return redirect("post_detail", post_id=post.id)
    else:
        form = CommentForm()

    return render(
        request,
        template_name="pages/partials/comment_list.html",
        context={"post": post, "form": form},
    )


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.author != request.user:
        messages.error(request, "Нельзя удалить чужой комментарий")
        return HttpResponseForbidden("У вас нет прав на удаление этого комментария")

    post = comment.post_id
    comment.delete()
    return redirect("post_detail", post_id=post.id)

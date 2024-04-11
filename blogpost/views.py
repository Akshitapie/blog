from django.shortcuts import render, redirect
from .models import Blog, Comment, Tag, Category, post, Materializedviewsblog
from django.contrib import messages
from django.db import transaction
import datetime


def index(request):
    blogdata = Blog.objects.all()
    catedata = Category.objects.all()
    return render(request, "index.html", {"blogdata": blogdata, "catedata": catedata})


def mateview(request):
    catedata = Category.objects.all()
    blogdata = Materializedviewsblog.objects.all()
    return render(
        request, "mateview.html", {"blogdata": blogdata, "catedata": catedata}
    )


def details(request, id):
    blogdata = Blog.objects.get(id=id)
    print("blog:", blogdata)
    comments = blogdata.comment_set.all()  # blogwise comment
    print("comments:", comments)

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        comment = request.POST.get("comment")

        comment = Comment(name=name, email=email, comments=comment, blog_id=blogdata)
        comment.save()

        return redirect("details", id=id)

    return render(request, "details.html", {"blog": blogdata, "comments": comments})


def add(request):
    tagdata = Tag.objects.all()
    cate = Category.objects.all()
    return render(request, "add.html", {"tagdata": tagdata, "cate": cate})


def insert(request):
    if request.method == "POST":
        try:
            title = request.POST.get("title")
            description = request.POST.get("description")
            pub_date = request.POST.get("pub_date")
            blog_image = request.FILES.get("blog_image")
            author_name = request.POST.get("author_name")
            email = request.POST.get("email")
            tagdata = request.POST.getlist("tag_title")  # getlist (get multiple data)
            print("tag :", tagdata)
            category_id = request.POST.get("cate_title_id")  # get 1 category
            print("category id:", category_id)
            cate_title_id = Category.objects.get(id=category_id)
            blogdata = Blog.objects.create(
                title=title,
                description=description,
                pub_date=pub_date,
                author_name=author_name,
                email=email,
                cate_title_id=cate_title_id,
                blog_image=blog_image,
            )
            for tag_id in tagdata:
                tag = Tag.objects.get(id=tag_id)
                blogdata.tag_title.add(tag)

            messages.success(request, " blog added successfully. !")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")

        return render(request, "add.html")


def update(request, id):
    blogdata = Blog.objects.get(id=id)
    return render(request, "update.html", {"blogdata": blogdata})


def edit(request, id):
    try:
        b1 = request.POST["title"]
        b2 = request.POST["description"]
        b3 = request.POST["pub_date"]
        b4 = request.POST["author_name"]
        b5 = request.POST["email"]
        with transaction.atomic():
            blogdata = Blog.objects.get(id=id)
            blogdata.title = b1
            blogdata.description = b2
            blogdata.pub_date = b3
            blogdata.author_name = b4
            blogdata.email = b5
            blogdata.save()
        messages.success(request, " blog updated successfully. !")
    except Exception as e:
        messages.error(request, f"An error occurred: {e}")
    return render(request, "update.html", {"blogdata": blogdata})


def tag(request):
    return render(request, "tag.html")


def addtag(request):
    tag_title = request.POST["tag_title"]
    tag = Tag(tag_title=tag_title)
    tag.save()
    return render(request, "tag.html")


def latestblog(request):
    blogdata = Blog.objects.order_by("-id")[:5]  # top 5 blog
    return render(request, "latestblog.html", {"blogdata": blogdata})


def categorywise(request, id):
    blogdata = Category.objects.get(id=id).blog_set.all()  # category wise blog
    return render(request, "categorywise.html", {"blogdata": blogdata})


def addpost(request):
    return render(request, "addpost.html")


def insertpost(request):
    title = request.POST["title"]
    description = request.POST["description"]
    pub_date = request.POST["pub_date"]
    author_name = request.POST["author_name"]
    blog_image = request.FILES["blog_image"]
    cate_title_id = request.POST["cate_title_id"]
    tag_title = request.POST["tag_title"]
    name = request.POST["name"]
    email = request.POST["email"]
    comments = request.POST["comments"]
    p = post(
        title=title,
        description=description,
        pub_date=pub_date,
        author_name=author_name,
        blog_image=blog_image,
        cate_title_id=cate_title_id,
        tag_title=tag_title,
        name=name,
        email=email,
        comments=comments,
    )
    p.save()
    return render(request, "addpost.html")


def allpost(request):
    postdata = post.objects.all()
    return render(request, "allpost.html", {"postdata": postdata})


def alldatablog(request):
    postdata = Blog.objects.all()

    return render(request, "alldatablog.html", {"postdata": postdata})


# # # filter data - date
# def allpost(request):
#     postdata = post.objects.filter(pub_date__gte=datetime.date(2024, 3, 24))
#     return render(request, "allpost.html", {"postdata": postdata})


# # filter data - title
# def allpost(request):
#     postdata = post.objects.filter(title__contains="Blog 1")
#     return render(request, "allpost.html", {"postdata": postdata})

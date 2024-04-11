from django.db import models
from tinymce import models as tinymce_models
from django.db.models.indexes import Index
from django.contrib.postgres.indexes import HashIndex, GinIndex, GistIndex


class AbstractData(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Tag(models.Model):
    tag_title = models.CharField(max_length=40)


class Category(models.Model):
    cate_title_id = models.CharField(max_length=40)

    class Meta:
        indexes = [GinIndex(fields=("cate_title_id",))]


class Blog(AbstractData):
    title = models.CharField(max_length=30)
    description = tinymce_models.HTMLField()
    pub_date = models.DateField()
    author_name = models.CharField(max_length=40)
    email = models.EmailField()
    tag_title = models.ManyToManyField(Tag)
    cate_title_id = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, default=0
    )
    blog_image = models.ImageField(upload_to="images/", default="default.jpg")

    def uppertext(self):  # custom method for blog title
        return self.title.upper()

    def commcount(self):  # custom method for blog title
        return self.comment_set.count()

    """Add indexes for title fields where title  display with ascending order"""

    class Meta:
        indexes = [models.Index(fields=["title"])]
        ordering = ["title"]


class Comment(AbstractData):
    blog_id = models.ForeignKey(Blog, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    email = models.EmailField()
    comments = models.CharField(max_length=50)

    """Add HashIndex for name fields where comments display with latest added comment"""

    class Meta:
        indexes = (HashIndex(fields=("name",)),)
        ordering = ["-id"]


class post(models.Model):
    title = models.CharField(max_length=30)
    description = tinymce_models.HTMLField()
    pub_date = models.DateField()
    author_name = models.CharField(max_length=40)
    blog_image = models.ImageField(upload_to="images/", default="default.jpg")
    tag_title = models.CharField(max_length=40)
    cate_title_id = models.CharField(max_length=40)
    name = models.CharField(max_length=40)
    email = models.EmailField()
    comments = models.CharField(max_length=50)

    """ Add indexes for pub_date and title """

    class Meta:
        indexes = [
            models.Index(
                fields=("pub_date", "title"),
            )
        ]


class Materializedviewsblog(models.Model):
    title = models.CharField(max_length=30)
    description = tinymce_models.HTMLField()
    pub_date = models.DateField()
    author_name = models.CharField(max_length=40)

    class Meta:
        managed = False  # This ensures Django doesn't manage this model's table
        db_table = "blogpost_materializedviewsblog"

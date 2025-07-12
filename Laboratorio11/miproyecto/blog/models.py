from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")
    slug = models.SlugField(unique=True, null=True)

    class Meta:
        verbose_name = "categoría"
        verbose_name_plural = "categorías"
        ordering = ['-created']

    def __str__(self):
        return self.name
        
    def get_absolute_url(self):
        return reverse('blog:category_detail', args=[self.slug or self.id])

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="Título")
    slug = models.SlugField(unique_for_date='published')
    content = models.TextField(verbose_name="Contenido")
    published = models.DateTimeField(verbose_name="Fecha de publicación", default=timezone.now)
    image = models.ImageField(
        upload_to="blog/%Y/%m/%d",
        null=True, 
        blank=True, 
        verbose_name="Imagen"
    )
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        verbose_name="Autor",
        related_name='blog_posts'
    )
    categories = models.ManyToManyField(
        Category, 
        verbose_name="Categorías", 
        related_name="blog_posts"
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    class Meta:
        verbose_name = "entrada"
        verbose_name_plural = "entradas"
        ordering = ['-published']
        indexes = [
            models.Index(fields=['-published']),
        ]

    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[
            self.published.year,
            self.published.month,
            self.published.day,
            self.slug
        ])
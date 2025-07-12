from django import template
from django.utils.safestring import mark_safe
import markdown

register = template.Library()

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))

@register.simple_tag
def total_posts():
    return Post.objects.count()

@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.objects.order_by('-published')[:count]
    return {'latest_posts': latest_posts}

    {% load blog_tags %}

<!-- Uso de filtro markdown -->
{{ post.content|markdown }}

<!-- Uso de simple tag -->
<p>Total de posts: {% total_posts %}</p>

<!-- Uso de inclusion tag -->
{% show_latest_posts 3 %}
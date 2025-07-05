from django.shortcuts import render, get_object_or_404
from .models import Article


def article_list(request):
    """
    Renders a page with a list of all articles.

    Args:
        request: HTTP request sent by the client.

    Returns:
        Response containing rendered template
        'articles/article_list.html' with context {'articles'}.
    """

    articles = Article.objects.all()
    return render(
        request,
        'articles/article_list.html',
        {'articles': articles}
    )


def article_detail(request, pk):
    """
    Renders the detail of a specific article according to the specified
    primary key.

    Args:
        request: HTTP request sent by the client.
        pk: The primary key of the article by which the record is searched.

    Returns:
        HttpResponse: Response containing rendered template
        'articles/article_detail.html' with context {'article'}.

    Raises:
        Http404: If an article with a given primary key does not exist.
    """

    article = get_object_or_404(Article, pk=pk)
    return render(
        request,
        'articles/article_detail.html',
        {'article': article}
    )

from django.db import models


class Article(models.Model):
    """
    Represents an article published on the website.

    Attributes
        - title (str): Article title, maximum 200 characters.
        - content (str): Article content of any length.
        - author (str): Author's name, maximum 100 characters.
        - created_at (datetime): The time the recording was created is set
          automatically.
        - updated_at (datetime): The time the record was last modified,
          updated automatically.

    Methods
        - __str__: Returns the article title as a text representation of the
          instance.
    """

    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Returns:
            str: Article name used, for example, in Django administration.
        """
        return self.title

from django.db import models


class Post(models.Model):
    title = models.TextField()
    content = models.TextField(blank=True, null=True)
    hidden = models.BooleanField(default=False)

    def get_absolute_url(self) -> str:
        return f"/blog/{self.pk}/"

    def __repr__(self):
        return f"{'' if self.hidden else '👀'}{self.__class__.__name__}(id={self.pk}, title={self.title!r})"

    __str__ = __repr__

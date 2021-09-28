from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse_lazy

User = get_user_model()


class Post(models.Model):
    title = models.TextField()
    content = models.TextField(blank=True, null=True)
    hidden = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self) -> str:
        return reverse_lazy("blog:single", kwargs={"pk": self.pk})

    def __repr__(self):
        return f"{'🔒' if self.hidden else ''}{self.__class__.__name__}(id={self.pk}, title={self.title!r})"

    __str__ = __repr__

from django.db import models


class Post(models.Model):
    title = models.TextField()
    content = models.TextField(blank=True, null=True)
    hidden = models.BooleanField(default=False)

    def get_absolute_url(self) -> str:
        return f"/blog/{self.pk}/"

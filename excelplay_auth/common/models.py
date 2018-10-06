from django.db import models


class User(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=100)
    profile_picture = models.URLField(null=False, blank=False)
    email = models.EmailField(null=False, blank=False)

    def __str__(self):
        return "<ID {} {}>".format(self.id, self.name)

    class Meta:
        ordering = ['id']
        verbose_name_plural = 'Users'

    
    @classmethod
    def create(cls, id, name, profile_picture, email):

        user = cls(id, name, profile_picture, email)
        user.save()

    @classmethod
    def all(cls):
        
        users = cls.objects.all()
        return users

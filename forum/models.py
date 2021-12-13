from django.db import models

# Create your models here.

# class Comment(models.Model):
#     content = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
#     phone_number = PhoneNumberField()
#     owner = models.ForeignKey(User,on_delete=models.CASCADE)

#     def get_absolute_url(self):
#         return reverse('view_post', kwargs={'post_id': self.post.id})
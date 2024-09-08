from django.db import models
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey

class AllowAuthor(models.Model):
    name = models.CharField(max_length=100) 
    
    def __str__(self):
        return self.name
        
class Authors(models.Model):
    name = models.CharField(max_length=100)  
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        if Authors.objects.filter(name=self.name).exists():
            raise ValidationError(f"An author with the name '{self.name}' already exists.")
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=100)    
    
    def __str__(self):
        return self.name
 
class Article(models.Model):
    author = models.ForeignKey(Authors, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=False, blank=False)
    sub_title = models.CharField(max_length=250, null=False, blank=False)
    image = models.ImageField(upload_to="article_img", null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    content = models.TextField()
    publish_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=[("draft", "Draft"), ("published", "Published")], default="draft")
    views = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.title} | {self.author}"
    
    class Meta:
        ordering = ['-publish_date']
        
class Comment(MPTTModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    article = models.ForeignKey('Article', related_name='comments', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    class MPTTMeta:
        order_insertion_by = ['created_at']
        
    def __str__(self):
        return f"{self.user} | {self.comment[0:30]}"
    
from django.db import models

# Create your models here.


class Category(models.Model):
    """
    model for category
    """
    category = models.CharField(max_length=200)

    def __str__(self):
        return self.category


class Author(models.Model):
    """
    model for authors
    """
    full_name = models.CharField(max_length=200)

    def __str__(self):
        return self.full_name


class Book(models.Model):
    """
    a model for our books
    """
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    inventory = models.IntegerField('Inventory',default=0)
    price = models.IntegerField('Price', default=0)
    image = models.ImageField(upload_to='book_pic/', default='./imgs/default_pic.png')
    document_addr = models.FileField(upload_to='documents/',blank=True,null=True)
    active = models.BooleanField(default=False, verbose_name='فعال / غیرفعال')

    def __str__(self):
        return self.title

    def update_inventory(self, amount):
        self.inventory += amount
        self.save()

    def update_price(self, cash):
        self.price += cash
        self.save()

    def delete(self):
        deleted_obj = f'{self.title} deleted'
        self.delete()
        return deleted_obj

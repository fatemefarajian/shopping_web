from django.urls import reverse
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)

    class Meta:
        ordering = ['name']
        indexes = [models.Index(fields=['name'])]
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='دسته بندی')
    name = models.CharField(max_length=250, verbose_name='نام محصول')
    slug = models.SlugField(max_length=250, unique=True, verbose_name='اسلاگ')
    description = models.TextField(verbose_name='توضیحات')
    inventory = models.PositiveIntegerField(default=0, verbose_name='موجودی')
    weight = models.PositiveIntegerField(default=0, verbose_name='وزن')

    #price
    price = models.PositiveIntegerField(default=0, verbose_name='قیمت')
    off = models.PositiveIntegerField(default=0, verbose_name='تخفیف')
    new_price = models.PositiveIntegerField(default=0, verbose_name='قیمت پس از تخفیف')

    #date
    created = models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')
    updated = models.DateTimeField(auto_now=True, verbose_name='تاریخ به روز رسانی')

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

    def get_absolute_url(self):
        return reverse('shop:product_detail', kwargs={'id': self.id, 'slug': self.slug})

    def __str__(self):
        return self.name


class ProductFeatures(models.Model):
    name = models.CharField(max_length=250, verbose_name='نام ویژگی')
    value = models.CharField(max_length=250, verbose_name='مقدار ویژگی')
    product = models.ForeignKey(Product, related_name='features', on_delete=models.CASCADE, verbose_name='محصول')

    def __str__(self):
        return self.name + ":" + self.value


class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images", verbose_name="محصول")
    file = models.ImageField(upload_to="product_images/%Y/%m/%d")
    title = models.CharField(max_length=250, verbose_name="عنوان", null=True, blank=True)
    description = models.TextField(verbose_name="توضیحات", null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]
        verbose_name = "تصویر"
        verbose_name_plural = "تصویر ها"

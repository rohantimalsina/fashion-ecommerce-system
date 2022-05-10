from django.db import models
from django.contrib.auth.models import User
from django.utils.html import mark_safe


# Details
class Detail(models.Model):
    email = models.EmailField()
    contact = models.CharField(max_length=12)
    address = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural='Details'

# Banner
class Banner(models.Model):
    img=models.ImageField(upload_to="banner/")
    alt_text=models.CharField(max_length=300)

    class Meta:
        verbose_name_plural='Banners'

    def image_tag(self):
        return mark_safe('<img src="%s" width="100" />' % (self.img.url))

    def __str__(self):
        return self.alt_text

# Category
class Category(models.Model):
    title=models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    image=models.ImageField(upload_to="category/")

    class Meta:
        verbose_name_plural='Categories'

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return self.title
    

# Product Model
class Product(models.Model):
    title=models.CharField(max_length=200)
    slug=models.CharField(max_length=255)
    image=models.ImageField(upload_to="product/",null=True)
    color=models.CharField(max_length=100)
    size=models.CharField(max_length=100)
    sku = models.CharField(max_length=255, unique=True)
    detail=models.TextField()
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    reg_price=models.PositiveIntegerField(default=0)
    sale_price=models.PositiveIntegerField(default=0)
    instock = models.IntegerField(default=100)
    status=models.BooleanField(default=True)
    is_featured=models.BooleanField(default=False)

    class Meta:
        verbose_name_plural='Products'

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))    

class Cart(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name="Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantity")
    total_amt=models.PositiveIntegerField(verbose_name="Total Amount")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    def __str__(self):
        return str(self.user)
    
    # Creating Model Property to calculate Quantity x Price
    @property
    def total_amt(self):
        return self.quantity * self.product.sale_price

# Order
STATUS_CHOICES = (
    ('Processing', 'Processing'),
    ('Shipped', 'Shipped'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled')
)

class Address(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    place = models.CharField(max_length=150, verbose_name="Nearest Place")
    city = models.CharField(max_length=150, verbose_name="City")
    state = models.CharField(max_length=150, verbose_name="State")
    class Meta:
        verbose_name_plural='Addresses'

    def __str__(self):
        return self.place

class Order(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    address = models.ForeignKey(Address, verbose_name="Shipping Address", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name="Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name="Quantity")
    price=models.PositiveIntegerField(verbose_name="Total Price")
    ordered_date = models.DateTimeField(auto_now_add=True, verbose_name="Ordered Date")
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=50,
        default="Pending"
        )


# Product Review
RATING=(
    (1,'1'),
    (2,'2'),
    (3,'3'),
    (4,'4'),
    (5,'5'),
)
class ProductReview(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    review_text=models.TextField()
    review_rating=models.CharField(choices=RATING,max_length=150)

    class Meta:
        verbose_name_plural='Reviews'

    def get_review_rating(self):
        return self.review_rating

# WishList
class Wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural='Wishlist'







   





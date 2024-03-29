from django.contrib import admin
from .models import *


class DetailsAdmin(admin.ModelAdmin):
	list_display=('email','contact','address')
class BannerAdmin(admin.ModelAdmin):
	list_display=('alt_text','image_tag')


class CategoryAdmin(admin.ModelAdmin):
	list_display=('title','image_tag')


class ColorAdmin(admin.ModelAdmin):
	list_display=('title','color_bg')


class ProductAdmin(admin.ModelAdmin):
    list_display=('id','title','image_tag','category','reg_price','sale_price','size','color','status','is_featured')
    list_editable=('sale_price','status','is_featured','size')
    prepopulated_fields = {"slug": ("title", )}



class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'created_at')
    list_editable = ('quantity',)
    list_filter = ('created_at',)
    list_per_page = 20
    search_fields = ('user', 'product')

class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'place', 'city', 'state')
    list_filter = ('city', 'state')
    list_per_page = 10
    search_fields = ('place', 'city', 'state')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'status', 'ordered_date','price')
    list_editable = ('quantity', 'status')
    list_filter = ('status', 'ordered_date')
    list_per_page = 20
    search_fields = ('user', 'product')

class ProductReviewAdmin(admin.ModelAdmin):
	list_display=('user','product','review_text','get_review_rating')

admin.site.register(Detail,DetailsAdmin)
admin.site.register(Banner,BannerAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(ProductReview,ProductReviewAdmin)
admin.site.register(Wishlist)

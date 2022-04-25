from django.shortcuts import render,redirect,  get_object_or_404
from django.db.models import Max,Min,Count,Avg
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import *
from .models import *
import decimal
from django.contrib.auth.models import User
from accounts.views import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def home(request):
   
    banners=Banner.objects.all().order_by('-id')
    data=Product.objects.filter(is_featured=True).order_by('-id')
    details=Detail.objects.all().order_by('-id')
    return render(request,'index.html',{'data':data,'banners':banners,'details':details})


# Category
def category_list(request):
    data=Category.objects.all().order_by('-id')
    return render(request,'category_list.html',{'data':data})

# Product List
def product_list(request):
    total_data=Product.objects.count()
    data=Product.objects.all().order_by('-id')[:3]
    min_price=ProductAttribute.objects.aggregate(Min('price'))
    max_price=ProductAttribute.objects.aggregate(Max('price'))
    return render(request,'product_list.html',
        {
            'data':data,
            'total_data':total_data,
            'min_price':min_price,
            'max_price':max_price,
        }
        )

# Product List According to Category
def category_product_list(request,cat_id):
    category=Category.objects.get(id=cat_id)
    data=Product.objects.filter(category=category).order_by('-id')
    return render(request,'category_product_list.html',{
            'data':data,
            })

def product_detail(request, slug,id):
    details=Detail.objects.all().order_by('-id')
    product = get_object_or_404(Product, slug=slug,id=id)
    related_products = Product.objects.exclude(id=product.id).filter(category=product.category)
    colors=ProductAttribute.objects.filter(product=product).values('color__id','color__title','color__color_code').distinct()
    sizes=ProductAttribute.objects.filter(product=product).values('size__id','size__title','color__id').distinct()
    reviewForm=ReviewAdd()

    # Check
    canAdd = False
    orderstat = Order.objects.filter(product=product,status="Delivered").count()
    if orderstat > 0:
        canAdd=True
    reviewCheck=ProductReview.objects.filter(product=product).count()
    
    if reviewCheck > 0:
        canAdd=False
    
    # End

    # Fetch reviews
    reviews=ProductReview.objects.filter(product=product)
    # End

    # Fetch avg rating for reviews
    avg_reviews=ProductReview.objects.filter(product=product).aggregate(avg_rating=Avg('review_rating'))
    # End

    return render(request, 'store/product_details.html',{'details':details,'product':product,'related':related_products,'colors':colors,'sizes':sizes,'reviewForm':reviewForm,'canAdd':canAdd,'reviews':reviews,'avg_reviews':avg_reviews})

# # Product Detail
# def product_detail(request,slug,id):
#     details=Detail.objects.all().order_by('-id')
#     product=Product.objects.get(id=id)
#     related_products=Product.objects.filter(category=product.category).exclude(id=id)[:4]
#     colors=ProductAttribute.objects.filter(product=product).values('color__id','color__title','color__color_code').distinct()
#     sizes=ProductAttribute.objects.filter(product=product).values('size__id','size__title','color__id').distinct()
#     reviewForm=ReviewAdd()

#     # Check
#     canAdd = False
#     orderstat = Order.objects.filter(product=product,status="Delivered").count()
#     if orderstat > 0:
#         canAdd=True
#     reviewCheck=ProductReview.objects.filter(product=product).count()
    
#     if reviewCheck > 0:
#         canAdd=False
    
#     # End

#     # Fetch reviews
#     reviews=ProductReview.objects.filter(product=product)
#     # End

#     # Fetch avg rating for reviews
#     avg_reviews=ProductReview.objects.filter(product=product).aggregate(avg_rating=Avg('review_rating'))
#     # End
    

#     return render(request, 'store/product_details.html',{'details':details,'data':product,'related':related_products,'colors':colors,'sizes':sizes,'reviewForm':reviewForm,'canAdd':canAdd,'reviews':reviews,'avg_reviews':avg_reviews})

def add_to_cart(request):
    if request.user.is_authenticated:
        user=request.user
        product_id = request.GET.get('prod_id')
        product = get_object_or_404(Product, id=product_id)

    # Check whether the Product is alread in Cart or Not
        item_already_in_cart = Cart.objects.filter(product=product_id, user=user)
        if item_already_in_cart:
            cp = get_object_or_404(Cart, product=product_id, user=user)
            cp.quantity += 1
            cp.save()
        else:
            Cart(user=user, product=product).save()
    
        return redirect('cart')

    else:
        messages.error(request,"Please login first.")
        return redirect('signin')

def cart(request):
    user = request.user
    cart_products = Cart.objects.filter(user=user)

    # Display Total on Cart Page
    amount = decimal.Decimal(0)
    shipping_amount = decimal.Decimal(10)
    # using list comprehension to calculate total amount based on quantity and shipping
    cp = [p for p in Cart.objects.all() if p.user==user]
    if cp:
        for p in cp:
            temp_amount = (p.quantity * p.product.price)
            amount += temp_amount

    # Customer Addresses
    addresses = Address.objects.filter(user=user)
    details=Detail.objects.all().order_by('-id')
    context = {
        'cart_products': cart_products,
        'amount': amount,
        'shipping_amount': shipping_amount,
        'total_amount': amount + shipping_amount,
        'addresses': addresses,
        'details' : details,
    }
    return render(request, 'store/cart.html', context)
    
    

def checkout(request):
    details=Detail.objects.all().order_by('-id')
    user = request.user
    address_id = request.GET.get('address')
    
    address = get_object_or_404(Address, id=address_id)
    # Get all the products of User in Cart
    cart = Cart.objects.filter(user=user)
    for c in cart:
        # Saving all the products from Cart to Order
        Order(user=user, address=address, product=c.product, quantity=c.quantity).save()
        # And Deleting from Cart
        c.delete()
    
    return render(request, 'store/checkout.html', {'details':details})  

def orders(request):
    details=Detail.objects.all().order_by('-id')
    all_orders = Order.objects.filter(user=request.user).order_by('-ordered_date')
    return render(request, 'store/orders.html', {'orders': all_orders, 'details':details})

# Save Review
def save_review(request,pid):
    product=Product.objects.get(pk=pid)
    user=request.user
    review=ProductReview.objects.create(
        user=user,
        product=product,
        review_text=request.POST['review_text'],
        review_rating=request.POST['review_rating'],
        )
    data={
        'user':user.username,
        'review_text':request.POST['review_text'],
        'review_rating':request.POST['review_rating']
    }

    # Fetch avg rating for reviews
    avg_reviews=ProductReview.objects.filter(product=product).aggregate(avg_rating=Avg('review_rating'))
    # End

    return JsonResponse({'bool':True,'data':data,'avg_reviews':avg_reviews})




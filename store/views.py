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
from django.db.models import Q
from .forms import AddressForm

from django.views import View

def home(request):
    banners=Banner.objects.all().order_by('-id')
    data=Product.objects.filter(is_featured=True).order_by('-id')
    category=Category.objects.all().order_by('-id')[:8]
    details=Detail.objects.all().order_by('-id')

    return render(request,'index.html',{'data':data,'category':category,'banners':banners,'details':details})

# Category
def category_list(request):
    data=Category.objects.all().order_by('-id')
    details=Detail.objects.all().order_by('-id')
    return render(request,'category_list.html',{'data':data,'details':details})

# Product List
def product_list(request):
    total_data=Product.objects.count()
    data=Product.objects.all().order_by('-id')
    details=Detail.objects.all().order_by('-id')
    return render(request,'store/product_list.html',
        {
            'data':data,
            'total_data':total_data,
            'details':details,
        }
        )



# Product List According to Category
def category_products(request,cat_id):
    category=Category.objects.get(id=cat_id)
    data=Product.objects.filter(category=category).order_by('-id')
    details=Detail.objects.all().order_by('-id')
    return render(request,'store/category_products.html',{
            'data':data,'details':details
            })

def product_detail(request, slug,id):
    details=Detail.objects.all().order_by('-id')
    product = get_object_or_404(Product, slug=slug,id=id)
    related_products = Product.objects.exclude(id=product.id).filter(category=product.category)[:4]
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
    # 
    reviews=ProductReview.objects.filter(product=product)
    # End
    review_count=ProductReview.objects.filter(product=product).count()

    # Fetch avg rating for reviews
    avg_reviews=ProductReview.objects.filter(product=product).aggregate(avg_rating=Avg('review_rating'))
    # End

    return render(request, 'store/product_details.html',{'details':details,'product':product,'related':related_products,'reviewForm':reviewForm,'canAdd':canAdd,'reviews':reviews,'avg_reviews':avg_reviews,'review_count':review_count})



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
    if request.user.is_authenticated:
        user=request.user
        cart_products = Cart.objects.filter(user=user)

    # Display Total on Cart Page
        amount = decimal.Decimal(0)
        shipping_amount = decimal.Decimal(100)
    # using list comprehension to calculate total amount based on quantity and shipping
        cp = [p for p in Cart.objects.all() if p.user==user]
        if cp:
            for p in cp:
                temp_amount = (p.quantity * p.product.sale_price)
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

    else:
        messages.error(request, "Please login to continue")
        return redirect ('signin')

# Cart quantity

def remove_cart(request, cart_id):
    if request.method == 'GET':
        c = get_object_or_404(Cart, id=cart_id)
        c.delete()
        messages.success(request, "Product removed from Cart.")
    return redirect('cart')


@login_required
def plus_cart(request, cart_id):
    if request.method == 'GET':
        cp = get_object_or_404(Cart, id=cart_id)
        cp.quantity += 1
        cp.save()
    return redirect('cart')


@login_required
def minus_cart(request, cart_id):
    if request.method == 'GET':
        cp = get_object_or_404(Cart, id=cart_id)
        # Remove the Product if the quantity is already 1
        if cp.quantity == 1:
            cp.delete()
        else:
            cp.quantity -= 1
            cp.save()
    return redirect('cart')
    
    

def checkout(request):
    details=Detail.objects.all().order_by('-id')
    user = request.user
    address_id = request.GET.get('address')
    
    address = get_object_or_404(Address, id=address_id)
    # Get all the products of User in Cart
    cart = Cart.objects.filter(user=user)
    for c in cart:
        # Saving all the products from Cart to Order
        Order(user=user, address=address, product=c.product, quantity=c.quantity,price=c.total_amt).save()
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



def add_to_wishlist(request):
    if request.user.is_authenticated:
        user=request.user
        product_id = request.GET.get('prod_id')
        product = get_object_or_404(Product, id=product_id)

    # Check whether the Product is alread in wishlist or Not
        item_already_in_wishlist = Wishlist.objects.filter(product=product_id, user=user)
        if item_already_in_wishlist:
            cp = get_object_or_404(Wishlist, product=product_id, user=user)
            cp.save()
            messages.error(request, "Item already in wishlist.")
        else:
            Wishlist(user=user, product=product).save()
    
        return redirect('home')

    else:
        messages.error(request,"Please login first.")
        return redirect('signin')


def wishlist(request):
    if request.user.is_authenticated:
        user=request.user
        wishlist_products = Wishlist.objects.filter(user=user)

        details=Detail.objects.all().order_by('-id')
    
        context = {
            'wishlist_products': wishlist_products,
            'details' : details,
        }
        
        return render(request, 'store/wishlist.html', context)

    else:
        messages.error(request, "Please login to continue")
        return redirect ('signin')

def remove_wishlist(request, wishlist_id):
    if request.method == 'GET':
        c = get_object_or_404(Wishlist, id=wishlist_id)
        c.delete()
        messages.success(request, "Product removed from wishlist.")
    return redirect('wishlist')

# Search
def search(request):
    keyword=request.GET['keyword']
    data=Product.objects.filter(Q(title__icontains=keyword) | Q(detail__icontains=keyword) | Q(slug__icontains=keyword)).order_by('-id')
    details=Detail.objects.all().order_by('-id')
    return render(request,'store/search.html',{'data':data,'details':details})

# Save addressbook
def save_address(request):
    
    if request.method=='POST':
        form=AddressForm(request.POST)
        if form.is_valid():
            saveForm=form.save(commit=False)
            saveForm.user=request.user
        
            saveForm.save()
            
    form=AddressForm
    return render(request, 'accounts/add_address.html',{'form':form})


# Update addressbook
def update_address(request,id):
    address=Address.objects.get(pk=id)
    
    if request.method=='POST':
        form=AddressForm(request.POST,instance=address)
        if form.is_valid():
            saveForm=form.save(commit=False)
            saveForm.user=request.user
            
            saveForm.save()
            messages.success(request, "You address has been updated.")
            return redirect('myaccount')
            
    form=AddressForm(instance=address)
    return render(request, 'accounts/update-address.html',{'form':form})

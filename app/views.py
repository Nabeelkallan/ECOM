from django.db.models import Count
from django.shortcuts import render,redirect
from django.views import View
from . models import Product,Customer,Cart
from . forms import RegistrationForm,LoginForm,ProfileForm
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request,"app/home.html")

def about(request):
    return render(request,"app/about.html")

def contact(request):
    return render(request,"app/contact.html")


class CategoryView(View):
    def get(self,request,val):
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request,"app/category.html",locals())
    
class CategoryTitle(View):
    def get(self,request,val):
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        return render(request,"app/category.html",locals())


class ProductDetail(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        return render(request,"app/productdetail.html",locals())
    
class RegistrationView(View):
    def get(self,request):
        form=RegistrationForm()
        return render(request,'app/registration.html',locals())
    def post(self,request):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"User Register Successfully")
        else:
            messages.warning(request,"Invalid Input")
        return render(request,'app/registration.html',locals())

class LoginView(View):
    def post(self,request):
        form=LoginForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Login Successfully")
            
        else:
            messages.warning(request,"Invalid Input")
        return render(request,'app/login.html',locals())

class ProfileView(View):
    def get(self,request):
        form = ProfileForm()
        return render(request,'app/profile.html',locals())
    def post(self,request):
        form=ProfileForm(request.POST)
        if form.is_valid():
            user=request.user
            name=form.cleaned_data['name']
            mobile=form.cleaned_data['mobile']
            city=form.cleaned_data['city']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']

            reg=Customer(user=user,name=name,mobile=mobile,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,"congratulations! Profile Save Successfully")
        else:
            messages.error(request,"Invalid Input Data")
        return render(request,'app/profile.html',locals())

def address(request):
    add=Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',locals())

class UpdateAddress(View):
    def get(self,request,pk):
        add=Customer.objects.get(pk=pk)
        form=ProfileForm(instance=add)
        return render(request,'app/updateaddress.html',locals())
    def post(self,request,pk):
        form=ProfileForm(request.POST)
        if form.is_valid():
            add=Customer.objects.get(pk=pk)
            add.name=form.cleaned_data['name']
            add.mobile=form.cleaned_data['mobile']
            add.city=form.cleaned_data['city']
            add.state=form.cleaned_data['state']
            add.zipcode=form.cleaned_data['zipcode']
            add.save()
            messages.success(request,"Congratulations! Profile update Successfully")
        else:
            messages.error(request,"Invalid Input Data")
        return redirect("address")

def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')

def show_cart(request):
    user=request.user
    cart=Cart.objects.filter(user=user)
    return render(request,'app/addtocart.html',locals())
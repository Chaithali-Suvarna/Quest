import requests
from bs4 import BeautifulSoup
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from . import models
from .models import Post,Signup,Login
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from .forms import PostForm


BASE_CRAIGSLIST_URL = 'https://www.craigslist.org/search/?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'


def adv(request):
    return render(request, 'adv.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("post")
        else:
            messages.info(request, 'Invalid Credentials!!!')
            return redirect('login')
    else:
          return render(request, 'login.html')

def base(request):
    return render(request, 'base.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username is already taken!')
            return redirect('signup')
        elif User.objects.filter(email=email).exists():
            messages.info(request, 'Email is already Taken!')
            return redirect('signup')
        else:

         user = User.objects.create_user(username=username, email=email, password=password)
         user.save();
         messages.info(request,'User Created')
         return redirect('signup')

    else:
         return render(request, 'signup.html')

def post(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        phone = request.POST['phone']
        country = request.POST['country']
        city = request.POST['city']
        category = request.POST['category']
        posttitle = request.POST['posttitle']
        description = request.POST['description']
        image = request.FILES['image']
        price = request.POST['price']

        post = Post(firstname=firstname, lastname=lastname,email=email, phone=phone,
                    country=country, city=city, category=category, posttitle=posttitle, description=description,image=image,price=price)
        post.save();
        messages.info(request, "You've Successfully Posted!")
        return redirect('post')

    else:
        return render(request, 'post.html')

def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = BASE_CRAIGSLIST_URL.format(search)
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data,'html.parser')

    post_listings = soup.find_all('li', {'class': 'result-row'})

    final_postings = []

    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')

        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'

        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
            print(post_image_url)
        else:
            post_image_url = 'https://craigslist.org/images/peace.jpg'

        final_postings.append((post_title, post_url, post_price, post_image_url))

    frontend = {
        'search': search,
        'final_postings': final_postings,
    }
    return render(request, 'new_search.html', frontend)

def logout(request):
    auth.logout(request)
    return redirect('/')

def search(request):
    if request.method == 'POST':
        srch = request.POST['srh']
        #print(srch)

        if srch:
            match = Post.objects.filter(Q(firstname__icontains=srch) | Q(city__icontains=srch) | Q(posttitle__icontains=srch) )
            #print(match)
            if match:
                return render(request, 'search.html', {'sr':match})
            else:
                messages.error(request,'No result found!')
        else:
            return redirect('search')
    return render(request, 'search.html')

def update(request,pk):
    post = Post.objects.get(id=pk)
    form = PostForm(instance=post)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
           form.save()
           return redirect('search')
    context = {'form': form}
    return render(request,'update.html', context)

def delete(request,id):
    post = Post.objects.get(id=id)
    post.delete()
    return redirect('search')

def contribution(request):
    post = Post.objects.all()
    return render(request,'contribution.html', {'post':post})

from django.shortcuts import render
from django.views.generic import TemplateView,CreateView
from .models import *
from django.urls import reverse_lazy
from django.core.paginator import Paginator
import requests
from django.http import JsonResponse
import json
from django.shortcuts import render,get_object_or_404,redirect
from .forms import CommentForm



################  Index qisim ###################

# Qidiruv qismi Poisk
def index(request):
	if request.user.is_authenticated:
		customer = request.user
		print(request.user)
		order,created = Order.objects.get_or_create(customer=customer,complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
		cxt = {
		'cartItems': cartItems
		}
	
	else:
		items = []
		order = {'get_cart_total': 0,'get_cart_items': 0}
		cartItems = order['get_cart_items']
		ctx = {
		'cartItems': cartItems
		}
	if 'q' in request.GET:
		q = request.GET['q']
		data = Menu.objects.filter(nomi__icontains=q)
	else:
		data = Menu.objects.all()


	context = {
		"data": data,
		"cartItems": cartItems
	}
	return render(request,"index.html",context)






class AboutPageView(TemplateView):
	template_name = 'about.html'


class ShopPageView(TemplateView):
	template_name = 'shop.html'




################  Create_product qisim ###################

"""admin bazaga malumot qoshish va admin bazadagi formani 
saytga ga formasini chaqirib beradi malumot qoshishlik un"""
class CreateProductView(CreateView):
	model = Menu 							#qatka qoshsin
	template_name = "create_product.html" 	#qaysi fayilga qoshsin
	fields = "__all__" 						# Bazadagi hamma ustunlarni olib chiqib berishi
	success_url =  reverse_lazy("index") 	# malumot qoshib bolgacha otkazib yuboradigan saxifa nomi







################  Contact qisim sms keluvchi ###################

def telegram(bot_message):
	bot_token =  '5555233935:AAElTmnzlc2wHf4af4nQLj7LjvT9Elsagqk' #BotFater ga kirib yoki yaratkan biron bir botimizni Tokenini olib qoyamiza
	bot_chatID = '503581054' #Bu yerga sms kimga kelishligi un keraklik odam id si qoyiladi
	send_text = 'https://api.telegram.org/bot'+bot_token+'/sendMessage?chat_id='+bot_chatID+'&parse_mode=Markdown&text='+bot_message
	response = requests.get(send_text)
	return response.json()




def contactPageView(request):
  if request.method == 'POST':
    name = request.POST.get('name',None)
    phone = request.POST.get('phone',None)
    email = request.POST.get('email',None)
    message = request.POST.get('message',None)
    user = Comment.objects.create(
      userName = name,
      phone = phone,
      email = email,
      message = message
    )
    user.save()
    telegram(f"ism:{name}\nTelefon raqam:{phone}\nEmail:{email}\nXabar:{message}")
  return render(
  request=request,
  template_name = 'contact.html'
  )




################  Glasses qisim ###################

#keyingi saxifaga otish funksiyasi
# def GlassesPageView(request):
# 	obj = Menu.objects.all()
# 	page_n = request.GET.get('page',1)
# 	p = Paginator(obj,5)
# 	try:
# 		page = p.page(page_n)
# 	except Exception:
# 		page = p.page(1)
# 	context = {
# 		"page":page
# 	}
# 	return render(request,"glasses.html",context)



"""registratsiydan otsa korzinkaga qoshadiga otmasa 
korzinka raqami 0 bolib turish un funksiya"""

def glassespageview(request):
    if request.user.is_authenticated:
        customer = request.user
        print(request.user)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        context = {
            'cartItems': cartItems
        }
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']
        context = {
            'cartItems': cartItems
        }

    obj = Menu.objects.all()
    page_n = request.GET.get('page', 1)
    p = Paginator(obj, 3)

    if 'q' in request.GET:
        q = request.GET['q']
        filtered_items = Menu.objects.filter(nomi__icontains=q)
        page = p.page(page_n)
        page.object_list = filtered_items
    else:
        page = p.page(page_n)

    context = {
        "page": page,
        "cartItems": cartItems
    }
    return render(request, "glasses.html", context)




"""Glaseesda korzinkaga maxsulot qoshib beradi"""
def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('bosildi',action)
	print('maxsulot id',productId)


	customer = request.user
	product = Menu.objects.get(id=productId)
	order,created = Order.objects.get_or_create(customer=customer,complete=False)
	orderItem,created = OrderItem.objects.get_or_create(order=order,product=product)

	if action == "add":
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == "remove":
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse("Item was adden",safe=False)






############ cart qisim Korzinka ustiga bosilganda ##############

def cardpageview(request):
	if request.user.is_authenticated:
		customer =  request.user
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		items = []
		order = {'get_cart_total': 0, "get_cart_items": 0}
		cartItems = order['get_cart_items']

	context = {
		"items": items,
		"order": order,
		'cartItems': cartItems } #necha marta bosilgani

	return render(request, 'cart.html', context)





def post_list(request):
	post = Post.objects.filter(moder=True)
	context = {
		"post":post
	}
	return render(request,'post_list.html',context)


def post_single(request,pk):
	post = get_object_or_404(Menu,pk=pk)
	comment = CommentPost.objects.filter(menu=post)
	if request.method == "POST":
		form = CommentForm(request.POST)
		if form.is_valid():
			comm = form.save(commit=False)
			comm.user = request.user
			comm.menu = post
			comm.save()
	else:
			form = CommentForm()
	ctx = {
		'post':post,
		'form':form,
		'comment':comment
	} 
	return render(request,'comments.html',ctx)














from django.db import models
from accounts.models import User

# MAXSULOTLAR BOLIMI
class Menu(models.Model):
	class Meta:
		db_table = 'menu'
		verbose_name = "maqola_menu"
		verbose_name_plural = "maqolalar_menu"
		ordering = ['create']

	nomi = models.CharField(max_length=250)
	malumot = models.TextField()
	narxi = models.FloatField(max_length=10)
	image =  models.ImageField(upload_to="imgaes/")
	create = models.DateTimeField(auto_now_add=True)
	update = models.DateTimeField(auto_now=True)
	moder = models.BooleanField(default=True)

	def __str__(self):
		return self.nomi



# SAYT CONTACT BOLIMI UN MODELS YANI TELEGRAMDAN SMS KELISHLIGI UN CLASS
class Comment(models.Model):
	userName = models.CharField(max_length=250)
	phone = models.CharField(max_length=20)
	email = models.CharField(max_length=50)
	message = models.TextField()
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.userName


#Korzinka chetidagi raqamga maxsulot qoshilsa ozgarishligi un va un hisoblash un models
class Order(models.Model):
	customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
	date_orderd = models.DateTimeField(auto_now_add=True)
	name = models.CharField(max_length=200, null=True)
	complete = models.BooleanField(default=False, null=True, blank=False)

	@property #dekarator
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total

	def __str__(self):
		return str(self.id)

class OrderItem(models.Model):
	product = models.ForeignKey(Menu, on_delete=models.SET_NULL, blank=True, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		total = self.product.narxi * self.quantity
		return total


	def __str__(self):
		return str(self.id)




class Post(models.Model):
	class Meta:
		db_table = 'post'
		verbose_name = "maqola"
		verbose_name_plural = "maqolalar"
		ordering = ['create']

	title = models.CharField(max_length=100)
	text = models.TextField()
	image = models.ImageField(upload_to='imgaes/', blank=True)
	create = models.DateTimeField(auto_now_add=True)
	update = models.DateTimeField(auto_now=True)
	moder = models.BooleanField(default=False)

	def __str__(self):
		return self.title





class CommentPost(models.Model):
	class Meta:
		db_table = 'comments'
		verbose_name = 'comment'
		verbose_name_plural = 'commentlar'

	user = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True, null=True) # Ikkta modelsni bir biriga ulash
	post = models.ForeignKey(Post,on_delete=models.SET_NULL,blank=True, null=True)
	menu = models.ForeignKey(Menu,on_delete=models.SET_NULL,blank=True,null=True)
	text = models.TextField(max_length=500)
	created = models.DateTimeField(auto_now_add=True)
	moder =  models.BooleanField(default=False) # True va False qiymat qaytarishi





class Category(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.name


class News(models.Model):
    title = models.CharField(max_length=250, null=False, blank=False)
    image = models.ImageField(upload_to="images/", blank=True)
    text = models.TextField()
    price = models.CharField(max_length=20)
    category = models.ForeignKey(Category, blank=False, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title










from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings
from .import views

urlpatterns = [
	path('', views.index,name='index'),
	path('about/',AboutPageView.as_view(),name='about'),
	path('contact/',contactPageView,name='contact'),
	path('glasses/',glassespageview,name='glasses'),
	path('shop/',ShopPageView.as_view(),name='shop'),
	path('create_product/',CreateProductView.as_view(),name='create_product'),
	path('update_item/',views.updateItem),
	path('card/',cardpageview,name='card'),
	path('comment/<int:pk>/',views.post_single,name="comment"),
	path('post_list/',post_list,name='post_list')
	# path('test/',TestPageView,name='test')
	
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)



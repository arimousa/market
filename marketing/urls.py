from django.contrib import admin
from django.urls import path, include
from market import views as market_views

urlpatterns = [
    path('', market_views.index, name='index'),
    path('admin/', admin.site.urls),
    path('product/', include('market.urls')),
    path('account/', include('users_app.urls')),
    path('contact', market_views.contact, name='contact'),
    path('about', market_views.about, name='about'),
    path('order', market_views.order, name='order'),
    path('shop', market_views.shop, name='shop'),
    path('buy/<product_code>', market_views.buy, name='buy_product'),
]

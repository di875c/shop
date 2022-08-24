from django.urls import path, include, re_path
from django.views.decorators.csrf import csrf_exempt
from . import views


urlpatterns = [
    path('', csrf_exempt(views.MainPage.as_view())),
    path('error/', csrf_exempt(views.ErrorView.as_view())),
    re_path(r'catalog/(?P<catalog_link>[a-z]+)', csrf_exempt(views.CatalogView.as_view())),
    re_path(r'product/(?P<product_link>[a-z,0-9]+)', csrf_exempt(views.ProductView.as_view())),
    path('contacts/', csrf_exempt(views.ContactView.as_view())),
    path('bracket/', csrf_exempt(views.BracketView.as_view())),
    path('gallery/', csrf_exempt(views.GalleryView.as_view())),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', csrf_exempt(views.SignView.as_view()), name='sign-view'),
    path('accounts/update/', csrf_exempt(views.user_change_settings), name='update-view'),
    path('search/', csrf_exempt(views.SearchResultView.as_view()), name='search_result'),
    # path('test/', csrf_exempt(views.TestView.as_view())),
]
from django.views import View, generic
from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Catalog, Product, Gallery, Bracket, User
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse_lazy
from .forms import SignUpForm, SelfUserChangeForm
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
from django.db.models import F, Q



class MainPage(View):
    def get(self, request, *args, **kwargs):
        catalogs = Catalog.objects.all()
        return render(request, 'first_page.html', {'catalogs': catalogs})

    def post(self, request, *args, **kwargs):
        try:
            email_data = request.POST
            if 'selfsend' in email_data: email_address = [email_data['email'], settings.EMAIL_HOST_USER]
            else: email_address = [settings.EMAIL_HOST_USER]
            text_email = email_data['textemail']
            text_email += '''\n телефон: {} \n адресс электронной почты: {}'''.format(email_data['phonenumber'], email_data['email'])
            headers = "Запрос от {} {} компания {}".format(email_data['name'], email_data['lastname'], email_data['companyname'])
            send_mail(headers, text_email, settings.EMAIL_HOST_USER, email_address)
            return HttpResponseRedirect('/')
        except: return HttpResponseRedirect('/error')


class CatalogView(View):
    def get(self, request, *args, **kwargs):
        cars = []
        catalogs = Catalog.objects.all()
        products = Catalog.objects.get(catalog_link=kwargs['catalog_link']).product.all()
        catalog_name = Catalog.objects.get(catalog_link=kwargs['catalog_link']).catalog_name
        for product in products:
            cars.append({
                'product': product,
                'main_image': product.gallery.get(main_image=True)
            })
        if len(products) == 0: products = []
        return render(request, 'catalog.html', {'catalogs': catalogs, 'products': cars, 'catalog_name': catalog_name})


class ProductView(View):
    def get(self, request, *args, **kwargs):
        catalogs = Catalog.objects.all()
        try:
            product = Product.objects.get(item_link=kwargs['product_link'])
            main_image = product.gallery.filter(main_image=True)[0]
        except: product = []
        print(product, kwargs['product_link'])
        return render(request, 'product.html', {'catalogs': catalogs, 'product': product, 'main_image':main_image})

    def post(self, request, *args, **kwargs):
        product_data = request.POST
        product_id = request.META['PATH_INFO'].split('/')[-1]
        item = Product.objects.get(item_link=product_id)
        try: user = User.objects.get(pk=request.user.pk)
        except: return HttpResponseRedirect('/accounts/login')
        print('Post_signal: ', product_data)
        if 'one_click' in request.POST: print('one_click', request.POST['one_click'])
        elif 'add_to_bracket' in request.POST:
            if Bracket.objects.filter(user=user, products=item):
                bracket_add = Bracket.objects.get(user=user, products=item)
                bracket_add.item_number += 1
                print(bracket_add)
                bracket_add.save()
            else:
                Bracket.objects.create(
                    user=user,
                    products=item,
                    item_number=1
                )
        return HttpResponseRedirect('/.')

class ErrorView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'error_page.html')


# class TestView(View):
#     def get(self, request, *args, **kwargs):
#         catalogs = Catalog.objects.all()
#         gallery = Gallery.objects.all()
#         if len(gallery) == 0: gallery = []
#         return render(request, 'test.html', {'catalogs': catalogs, 'gallery': gallery})


class GalleryView(View):
    def get(self, request, *args, **kwargs):
        catalogs = Catalog.objects.all()
        gallery = Gallery.objects.all()
        if len(gallery) == 0: gallery = []
        return render(request, 'gallery.html', {'catalogs': catalogs, 'gallery': gallery})


class ContactView(View):
    def get(self, request, *args, **kwargs):
        catalogs = Catalog.objects.all()
        return render(request, 'contact.html', {'catalogs': catalogs})


class BracketView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        catalogs = Catalog.objects.all()
        brackets = User.objects.get(pk=request.user.pk).bracket.filter(status=0)
        no_data = 'no_data' in kwargs
        return render(request, 'bracket.html', {'catalogs': catalogs, 'brackets': brackets,
            'user': User.objects.get(pk=request.user.pk), 'no_data': no_data})

    def post(self, request, *args, **kwargs):
        # try:
        bracket_data = request.POST
        # print(bracket_data)
        if 'email' in bracket_data:
            User.objects.filter(pk=request.user.pk).update(
                first_name=bracket_data['first_name'],
                last_name=bracket_data['last_name'],
                phone_number=bracket_data['phone_number'],
                email=bracket_data['email']
            )
            return HttpResponseRedirect('./')
        else:
            user = User.objects.get(pk=request.user.pk)
            if not user.email or not user.phone_number:
                print('NO DATA')
                return self.get(request, no_data=True)
            #в боевом режиме: send_mail(headers, text_email, settings.EMAIL_HOST_USER, email_address)
            [Bracket.objects.filter(pk=data[12:]).update(item_number=number, status=1) for data, number in bracket_data.items()]
            email_address = [user.email, settings.EMAIL_HOST_USER]
            text_email = '''\n телефон: {} \n адресс электронной почты: {}\nЗаказано:\n'''.format(user.phone_number, user.email)
            for item in user.bracket.filter(status=1):
                text_email += 'Машина - {} в количестве -{}\n'.format(item.products.item_name, item.item_number)
            headers = "Запрос от {} {}".format(user.first_name, user.last_name)
            print(user.bracket.filter(status=1))
            print(headers, text_email, settings.EMAIL_HOST_USER, email_address)
            return HttpResponseRedirect('../')
        # except: return HttpResponseRedirect('/error')


class SignView(generic.CreateView):
    #Create new user
    form_class = SignUpForm
    success_url = reverse_lazy('login') #To Do update page to render after success
    template_name = 'registration/signup.html'


class SearchResultView(generic.ListView):
    model = Product
    template_name = 'search_result.html'
    # queryset = Product.objects.filter(item_name='bmw X5')

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Product.objects.filter(
            Q(item_name__icontains=query) | Q(item_description__icontains=query)
        )
        print(object_list)
        return object_list


@login_required(login_url='/accounts/login')
def user_change_settings(request):
    #Update user profile
    template_name = 'registration/change_user.html'
    user = User.objects.get(pk=request.user.pk)
    if request.method == 'POST':
        form = SelfUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect(to='/')
    else:
        form = SelfUserChangeForm(instance=user)
    return render(request, template_name, {'form': form})

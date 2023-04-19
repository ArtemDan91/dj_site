from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseNotFound
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication, \
    SessionAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, \
    IsAuthenticated

from .forms import *
from women.permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from .utils import *
from .serializers import *


# class WomenVeiwSet(viewsets.ModelViewSet):
#     #queryset = Women.objects.all()
#     serializer_class = WomenSerializer
#
#     def get_queryset(self):
#         pk = self.kwargs.get('pk')
#         if not pk:
#             return Women.objects.all()[:3]
#         else:
#             return Women.objects.filter(pk=pk)
#
#     @action(methods=['get'], detail=True)
#     def category(self, request, pk=None):
#         cats = Category.objects.get(pk=pk)
#         return Response({'cats': cats.name})


class WomenAPIList(generics.ListCreateAPIView):
    queryset = Women.objects.all()
    serializer_class = WomenSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )


class WomenAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Women.objects.all()
    serializer_class = WomenSerializer
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, ) #доступ лише по токенам

class WomenAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Women.objects.all()
    serializer_class = WomenSerializer
    permission_classes = (IsAdminOrReadOnly, )


# class WomenAPIView(APIView):
#     def get(self, request):
#         w = Women.objects.all()
#         return Response({'posts': WomenSerializer(w, many=True).data})
#
#     def post(self, request):
#         serializer = WomenSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         # post_new = Women.objects.create(
#         #     title=request.data['title'],
#         #     slug=request.data['slug'],
#         #     content=request.data['content'],
#         #     cat_id=request.data['cat_id']
#         # )
#         # return Response({'post': WomenSerializer(post_new).data})
#         return Response({'post': serializer.data})
#
#     def put(self, request, *args, **kwargs):
#         pk = kwargs.get("pk", None)
#         if not pk:
#             return Response({"error": "Method PUT is not allowed"})
#         try:
#             instance = Women.objects.get(pk=pk)
#         except:
#             return Response({"error": "Object does not exist"})
#         serializer = WomenSerializer(data=request.data, instance=instance)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({'post': serializer.data})
#
#     def delete(self, request, *args, **kwargs):
#         pk = kwargs.get("pk", None)
#         if not pk:
#             return Response({"error": "Method DELETE is not allowed"})
#         try:
#             instance = Women.objects.get(pk=pk)
#             instance.delete()
#         except:
#             return Response({"error": "Object does not exist"})
#         return Response({'post': 'delete post ' + str(pk)})


class WomenHome(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Головна сторінка')
        return context | context_def
    def get_queryset(self):
        return Women.objects.filter(is_published=True).select_related('cat')

# def index(request):
#     posts = Women.objects.all()
#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': 'Головна сторінка',
#         'cat_selected': 0,
#     }
#     return render(request, 'women/index.html', context=context)


class WomenAbout(DataMixin, ListView):
    model = Women
    template_name = 'women/about.html'
    paginate_by = None

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Про сайт')
        return context | context_def


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    # login_url = '/admin/'
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Додавання статті')
        return context | context_def


# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#     return render(request, 'women/addpage.html', {'form':form, 'menu': menu, 'title': 'Додавання статті'})


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'women/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title="Зворотній зв'язок")
        return context | context_def

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')


# def contact(request):
#     return HttpResponse("Зворотній зв'язок")


class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title=context['post'].title)
        return context | context_def


# def show_post(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug)
#     context = {
#         'post': post,
#         'menu': menu,
#         'title': post.title,
#         'cat_selected': post.cat_id,
#     }
#     return render(request, 'women/post.html', context=context)


class WomenCategory(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        context_def = self.get_user_context(title='Категорія - ' + str(c.name), cat_selected=self.kwargs['cat_slug'])
        return context | context_def


    def get_queryset(self):
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

# def show_category(request, cat_slug):
#     posts = Women.objects.filter(cat__slug=cat_slug)
#
#     if len(posts) == 0:
#         raise Http404()
#
#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': 'Відображення по рубрикам',
#         'cat_selected': cat_slug,
#     }
#     return render(request, 'women/index.html', context=context)


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'women/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Реєстрація')
        return context | context_def

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'women/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Авторизація')
        return context | context_def

    def get_success_url(self):
        return reverse_lazy('home')

# def login(request):
#     return HttpResponse("Авторизація")


def logout_user(request):
    logout(request)
    return redirect('login')


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Сторінка не знайдена</h1>')
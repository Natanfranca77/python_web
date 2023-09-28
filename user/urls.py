from django.urls import path
from  django.views.decorators.csrf import csrf_exempt
from rest_framework.urlpatterns import format_suffix_patterns
from user.views import CreateUserView,AdminView,logoutView,CustomTokenView,UserViewPrivate


urlpatterns=[
    path("",csrf_exempt(CreateUserView.as_view())),
    path("token/",CustomTokenView.as_view()),
    path('editar/',UserViewPrivate.as_view()),
    path("admin/",AdminView.as_view(),name="list-user"),
    path("admin/<id>/",AdminView.as_view(),name="detail-user"),
    path("logout/",logoutView.as_view())

]

urlpatterns= format_suffix_patterns(urlpatterns)
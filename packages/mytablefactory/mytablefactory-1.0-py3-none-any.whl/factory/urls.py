"""factory URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
#router.register(r'tables', views.TableViewApi)
#router.register(r'tablesUpdate', views.TableUpdateSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tables.urls')),
    
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('api/tables/',views.TablesViewAllApi.as_view()),
    path('api/tables/create/',views.TableCreateApi.as_view()),
    path('api/tables/<int:pk>/',views.TableViewByIdApi.as_view()),
    path('api/tables/<int:pk>/update/',views.TableUpdateApi.as_view()),
    path('api/tables/<int:pk>/delete/',views.TableDeleteApi.as_view()),

    path('api/legs/',views.LegsViewAllApi.as_view()),
    path('api/legs/create/',views.LegCreateApi.as_view()),
    path('api/legs/<int:pk>/',views.LegViewByIdApi.as_view()),
    path('api/legs/<int:pk>/update/',views.LegUpdateApi.as_view()),
    path('api/legs/<int:pk>/delete/',views.LegDeleteApi.as_view()),

    path('api/feet/',views.FeetViewAllApi.as_view()),
    path('api/feet/create/',views.FootCreateApi.as_view()),
    path('api/feet/<int:pk>/',views.FootViewByIdApi.as_view()),
    path('api/feet/<int:pk>/update/',views.FootUpdateApi.as_view()),
    path('api/feet/<int:pk>/delete/',views.FootDeleteApi.as_view()),

]

from django.urls import path
from .import views
urlpatterns = [
    path('users/', views.MyUsersListView.as_view(), name='MyUsersListView'),
    path('user_add/', views.MyUsersAddView.as_view(), name='MyUsersAddView'),
    path('user_edit/', views.MyUsersEditView.as_view(), name='MyUsersEditView'),
    path('user_del/', views.MyUsersRemoveView.as_view(), name='MyUsersRemoveView'),

]
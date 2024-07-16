from django.urls import path
from .import views
urlpatterns = [
    path('asset_list/', views.AssetListView.as_view(), name='AssetListView'),
    path('asset_add/', views.AssetAddView.as_view(), name='AssetAddView'),
    path('asset_edit/', views.AssetEditView.as_view(), name='AssetEditView'),
    path('asset_edit_next/', views.AssetEditGetNextView.as_view(), name='AssetEditGetNextView'),
    path('demo_test/', views.DemoBaseTestView.as_view(), name='DemoBaseTestView'),

]
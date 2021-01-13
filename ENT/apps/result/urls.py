from django.urls import path

from . import views

app_name='result'
urlpatterns = [
	path('', views.index, name='index'),
	path('add/', views.add_person, name='add_person'),
	path('bb/', views.info, name='info'),
	path('<int:per_id>/', views.add_res, name='add_res'),
	path('bb/<int:tr_id>/', views.add_res_ent, name='add_res_ent')
]
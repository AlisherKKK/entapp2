from django.urls import path

from . import views

app_name = 'result'
urlpatterns = [
	path('', views.index, name='index'),
	path('for_admin/', views.admin, name='manpage'),
	path('admin_page/', views.add_admin, name='add_admin'),
	path('<int:ad_id>/', views.add_std_toadmin, name='add_std_toadmin'),
	path('admin_page/<int:adm_id>/', views.remove_std_fromadmin, name='remove_std_fromadmin'),
	path('add/', views.add_person, name='add_person'),
	path('bb/', views.info, name='info'),
	path('<int:per_id>/', views.add_res, name='add_res'),
	path('bb/<int:tr_id>/', views.add_res_ent, name='add_res_ent')
]
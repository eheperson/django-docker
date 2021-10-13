from django.urls import path

from . import views

app_name = 'polls'
#
urlpatterns = [
    path('', views.index, name='index'), # /polls/
    path('index/', views.index, name='index'), # /polls/index/
    path('rawindex/', views.rawindex, name='rawindex'), # /polls/rawindex/
    path('indexGeneric/', views.IndexView.as_view(), name='index'), # /polls/indexGeneric
    path('ehe/', views.ehe, name='ehe'), # /polls/ehe/
    path('info/', views.info, name='info'), # /polls/info
    path('<int:question_id>/', views.detail, name='detail'), # /polls/5/
    path('generic/<int:pk>/', views.DetailView.as_view(), name='detail'), # /polls/generic/5/
    path('<int:question_id>/results/', views.results, name='results'), # /polls/5/results/
    path('<int:pk>/resultsGeneric/', views.ResultsView.as_view(), name='results'), # /polls/5/resultsGeneric/
    path('<int:question_id>/vote/', views.vote, name='vote'), # /polls/5/vote/
]


from django.urls import path

from test_set.views import TestListView, TestRunView

app_name = 'tests'

urlpatterns = [
    path('', TestListView.as_view(), name='list'),
    path('<int:pk>/question/<int:seq_nr>', TestRunView.as_view(), name='testrun_step'),
    # path('<int:pk>/start', StartTestView.as_view(), name='start'),
]

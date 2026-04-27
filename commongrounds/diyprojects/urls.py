from django.urls import path
from .views import ProjectListView, ProjectDetailView
from .views import ProjectCreateView, ProjectUpdateView

app_name = "diyprojects"

urlpatterns = [
    path('projects', ProjectListView.as_view(), name='project_list'),
    path('project/<int:pk>/', ProjectDetailView.as_view(),
         name='project_detail'),
    path('project/add', ProjectCreateView.as_view(), name='project_add'),
    path('project/<int:pk>/edit', ProjectUpdateView.as_view(),
         name='project_edit'),
]

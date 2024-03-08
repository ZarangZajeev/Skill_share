from django.urls import path
from exam import views
from rest_framework.routers import DefaultRouter

from django.urls import path
from .views import download_answer

router=DefaultRouter()
router.register("topics",views.TopicAddView,basename="topic")
router.register("questions",views.ViewQuestionView,basename="questions")
router.register('answers',views.AnswerAddView, basename='answer')
# router.register('admin/download_answer/<int:answer_id>', download_answer, basename='download_answer')

from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
     path('add-question/',views.AddQuestionView.as_view(), name='add-question'),
     path('topics/<int:topic_id>/questions/', views.TopicQuestionsView.as_view(), name='topic-questions'),

     path('download_answer/<int:answer_id>/', download_answer, name='download_answer'),

]+router.urls
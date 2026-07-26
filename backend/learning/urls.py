from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='learning-dashboard'),
    path('courses/', views.courses, name='learning-courses'),
    path('course/<uuid:id>/', views.course_detail, name='learning-course-detail'),
    path('lesson/<uuid:id>/', views.lesson_detail, name='learning-lesson-detail'),
    path('lesson/<uuid:id>/complete/', views.complete_lesson, name='learning-lesson-complete'),
    path('quiz/<uuid:id>/submit/', views.submit_quiz, name='learning-quiz-submit'),
    path('recommendations/', views.recommendations, name='learning-recommendations'),
    path('progress/', views.progress, name='learning-progress'),
    path('course/<uuid:id>/reset/', views.reset_course, name='learning-course-reset'),
]

from django.urls import path, include

urlpatterns = [
    path('blog/', include(('devopsplayground.blog.urls', 'blog'))),
    path('users/', include(('devopsplayground.users.urls', 'users'))),
]

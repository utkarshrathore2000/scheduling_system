from django.urls import path, include
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from meetings.schema import schema
from .views import DashboardView, LoginView, logout, MyMeetingView

app_name = 'meetings'

urlpatterns = [
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema)), name='graphql_view'),
    path('dashboard/', DashboardView.as_view(), name="dashboard_view"),
    path('login/', LoginView.as_view(), name="login_view"),
    path("logout/", logout, name="logout_view"),
    path("my_meetings/", MyMeetingView.as_view(), name="my_meeting_view"),

]
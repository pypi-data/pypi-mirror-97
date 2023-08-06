from django.urls import include, path

app_name = 'tom_registration'


urlpatterns = [
    path('', include('tom_registration.registration_flows.open.urls', namespace='registration')),
    path('', include('tom_common.urls')),
]

from django.urls import include, path

app_name = 'tom_registration'

urlpatterns = [
    path('', include('tom_registration.registration_flows.approval_required.urls', namespace='registration')),
    path('', include('tom_common.urls')),
]

from django.urls import path

from tom_registration.registration_flows.approval_required.views import ApprovalRegistrationView, UserApprovalView
from tom_registration.registration_flows.open.views import OpenRegistrationView

app_name = 'tom_registration'


urlpatterns = [
    path('register/open/', OpenRegistrationView.as_view(), name='register-open'),
    path('register/approval/', ApprovalRegistrationView.as_view(), name='register-approval'),
    path('approve/<int:pk>/', UserApprovalView.as_view(), name='approve')
]

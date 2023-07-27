"""
URL configuration for MedicalProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from medical.views import (
    login,
    register,
    homepage,
    instruction,
    guess,
    microscope,
    inquiry,
    inquiryplus,
    user,
    illustration,
    submicroscope,
)

urlpatterns = [
    path("medical/login/", login),
    path("medical/register/", register),
    path("medical/homepage/", homepage),
    path("medical/instruction/", instruction),
    path("medical/guess/", guess),
    path("medical/microscope/<str:name>/", submicroscope),  # 疾病名作为参数
    path("medical/microscope/", microscope),
    path("medical/inquiry/", inquiry),
    path("medical/inquiryplus/", inquiryplus),
    path("medical/user/", user),
    path("medical/illustration/", illustration),
]

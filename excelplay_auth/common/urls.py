
from django.conf.urls import url
from .views import sign_out,sign_in

urlpatterns = [
	#url(r'signin', signin ),
	url(r'sign_in', sign_in ),
	url(r'sign_out', sign_out ),
]
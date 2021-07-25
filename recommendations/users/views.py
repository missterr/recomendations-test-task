import json
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.http.response import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from users.helpers import add_recommendations


class UserView(View):
    def get(self, request):
        """Supposed that add_recommendations can be invoked by schedule in real project"""
        add_recommendations(request.user)
        return JsonResponse({'recommendations': request.user.get_recommended()})


@method_decorator(csrf_exempt, name='dispatch')
class UserLogin(View):
    def post(self, request):
        form = AuthenticationForm(request, data=json.loads(request.body))
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return HttpResponse()
        else:
            return HttpResponse(form.errors, status=400)

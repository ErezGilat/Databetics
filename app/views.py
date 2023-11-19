from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.http import JsonResponse
from django.views.generic import (
    TemplateView, View
)
from .models import DIAGNOSE
from app import code
import requests
import json


class QuizView(TemplateView):
    template_name = 'app/quiz.html'
 
    def get(self, request):
        clientKey = request.GET.get('captcha', False)
        if not clientKey: return redirect('captcha')
        secretKey = "6LcweJ0iAAAAANtkQVQQnEXm314ieB68bvz31wxe"
        captchaData = {
            'secret': secretKey,
            'response': clientKey 
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=captchaData)
        response = json.loads(r.text)
        verify = response['success']
        if verify: 
            return super().get(request)
        else: 
            return redirect('captcha')


results = [
    'You probably don\'t have diabetes!',
    'You might have pre diabetes!, please consult your doctor',
    'You might have diabetes!, please consult your doctor asap!'
    ]
class QuizResult(View):
    def post(self, request):
        diagnose = DIAGNOSE()
        data = json.loads(request.POST.get('data'))
        diagnose.diagnosed = True if int(data['22']) == 1 else False
        del data['22']
        data = [{str(k): int(v) for k, v in data.items()}]
        diagnose.details = data
        print('Here: ', data)
        # print('\n\nData: \n', data)
        try:
            output = code.diagnose(data)[0]
            diagnose.output = output
            result = results[output]
        except Exception as e:
            result = 'Something Went Wrong.'
            print('\n\nError: \n', e)
        diagnose.result = result
        diagnose.save()
        return JsonResponse({'results': result}, safe=False)


class Captcha(TemplateView):
    template_name = "app/captcha.html"

    def post(self, request):
        clientKey = request.POST.get("g-recaptcha-response", False)
        # return redirect('quiz')
        if clientKey not in ['', ' ', False, None]: return redirect(f'/quiz/?captcha={clientKey}') 
        else: return redirect(request.path)

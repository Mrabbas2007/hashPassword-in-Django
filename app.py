from django.db import models

from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response

# set your models in 'models.py'.

class User(models.Model):
    name = models.CharField(max_length=100)
    uName = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=225)


# set urls in 'urls.py'

urlpatterns = [
    path('api/signup/', SignUp.as_view(), name="signup"),
    path('api/login/', Login.as_view(), name="login"),
]


# set your Views in 'views.py'

@method_decorator(csrf_exempt, name='dispatch')
class SignUp(APIView):
    def post(self, request):
        data = request.data
        st = 200
        if User.objects.filter(uName=data['uName']).first():
            st = 203
        elif User.objects.filter(email=data['email']).first():
            st = 204
        else :
            user = User(name=data['name'], uName=data['uName'], 
                        email=data['email'], password=make_password(data['password']))
            st = 200
            user.save()
        return Response({'message': 'Data received', 'data': data}, status=st)


class Login(APIView):
    def post(self, request):
        data = request.data

        try :
            if User.objects.filter(uName=data['uName']).first():
                user = User.objects.filter(uName=data['uName']).first()
                if check_password(data['password'], user.password) :
                    return Response({'message': 'Data received', 'data': data}, status=200)
                else :
                    return Response({'message': 'Data received', 'data': data}, status=202)
            else :
                return Response({'message': 'Data received', 'data': data}, status=201)
        except Exception as ex :
                return Response({'message': 'Data received', 'data': data}, status=505)




# this is a total project for [hash password] and [work with API]
# of course you must set somthing in setting.py



from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler
import pandas as pd
from .models import User
from diabetes.models import Diabetes


#loaded_model = joblib.load("machine.joblib", mmap_mode = None)
loaded_model = pickle.load(open('trained_model.sav','rb'))
data = pd.read_csv('diabetes.csv')
X = data.drop(columns = 'Outcome', axis = 1)
scaler = StandardScaler()
scaler.fit(X)

#@login_required(login_url='/diabetes/login/')
def signin(request):
  if request.method == "POST":
    username = request.POST['username']
    pass1 = request.POST['pass1']
    my_user = authenticate(username=username,password=pass1)
    if my_user is not None:
      login(request, my_user)
      return redirect('profile')
    else:
      messages.error(request,"bad credentials")
      return redirect('login')
    
  return render(request,'diabetes/login.html')


def register(request):
  if request.method =="POST":
    username = request.POST['username']
    fullname = request.POST['full_name']
    email = request.POST['email']
    pass1 = request.POST['pass1']
    pass2 = request.POST['pass2']
    my_user = User.objects.create_user(username,email,pass1)
    my_user.full_name = fullname
    my_user.save()
    messages.success (request,"your account has been created")
    return redirect('login')
    #return HttpResponse("success")
  return render(request,'diabetes/registration.html')

#loaded_model = joblib.load('machine.joblib')


# Create your views here.

@login_required(login_url='/diabetes/login')
def profile(request):
  
  return render(request,'diabetes/profile.html')

@login_required(login_url='/diabetes/login/')
def input1(request):
  if request.method == 'POST':
    Pregnancies = request.POST['Pregnancies']
    Glucose = request.POST['Glucose']
    BloodPressure = request.POST['BloodPressure']
    SkinThickness = request.POST['SkinThickness']
    Insulin = request.POST['Insulin']
    BMI = request.POST['BMI']
    DiabetesPedigreeFunction = request.POST['DiabetesPedigreeFunction']
    Age = request.POST['Age']

    
    
    array = np.asarray([[Pregnancies,Glucose,BloodPressure,SkinThickness,Insulin,BMI,DiabetesPedigreeFunction,Age]])
    r = array.reshape(1,-1)
    w = scaler.transform(r)
    pred = loaded_model.predict(w)
    if pred[0] == 0:
      pred= 'negative'
    else:
      pred= 'positive'

    diabetes_data = Diabetes(
      Pregnancies = Pregnancies,
      Glucose = Glucose,
      BloodPressure = BloodPressure,
      SkinThickness = SkinThickness,
      Insulin = Insulin,
      BMI = BMI,
      DiabetesPedigreeFunction = DiabetesPedigreeFunction,
      Age = Age,
      Result = pred
      
    )
    diabetes_data.user = request.user
    diabetes_data.save()
    
      

    return render(request,'diabetes/test_result.html',{'result': pred})
  return render(request,'diabetes/input1.html')

@login_required(login_url='/diabetes/login/')
def history(request):
  diabetes = Diabetes.objects.filter(user = request.user)
  return render(request,'diabetes/history.html',{'diabetes':diabetes})

@login_required(login_url='/diabetes/login/')
def calorie_calc(request):
  #ZyrM2BW1uQGQIJqW/6xzbA
  import json
  import requests
  if request.method == 'POST':
      query = request.POST['query']
      api_url = 'https://api.api-ninjas.com/v1/nutrition?query='
      api_request = requests.get(
          api_url + query, headers={'X-Api-Key': 'ZyrM2BW1uQGQIJqW/6xzbA==FYY2t8NXdwzPYvxJ'})
      try:
          food = json.loads(api_request.content)
          print(api_request.content)
      except Exception as e:
          food = "oops! There was an error"
          print(e)
      return render(request, 'diabetes/calorie_calc.html', {'food': food})
  else:
      return render(request, 'diabetes/calorie_calc.html', {'query': 'Enter a valid query'})


#@login_required(login_url='/diabetes/login/')
def signout(request):
  logout(request)
  return redirect('login')
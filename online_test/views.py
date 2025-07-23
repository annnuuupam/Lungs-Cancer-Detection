import os
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from online_test.models import *
from django.views.decorators.csrf import csrf_exempt #include this 
import random
import razorpay
from django.http import JsonResponse
import google.generativeai as ai
from django.http import JsonResponse
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier

from ots import settings
from .forms import BreastCancerForm, DiabetesForm, HeartDiseaseForm

def welcome(request):
    template=loader.get_template("welcome.html")
    res=template.render()
    return HttpResponse(res)

def signup(request):
    template=loader.get_template("signup.html")
    res=template.render()
    return HttpResponse(res)

@csrf_exempt # include  this
def store_user(request):
    if request.method=='POST':
        username=request.POST['username']
        if(len(User.objects.filter(username=username))):
            msg='username already taken ....try another username'
            context={
                'msg':msg
            }
            template=loader.get_template("signup.html")
            res=template.render(context,request)
            return HttpResponse(res)
        else:
            user=User() # insertion
            user.username=username
            user.password=request.POST['password']
            user.name=request.POST['name']
            user.save()
            template=loader.get_template("login.html")
            res=template.render()
            return HttpResponse(res)
    else:
        msg='invalid request......first signup'
        context={
            'msg':msg
        }
        template=loader.get_template("signup.html")
        res=template.render(context,request)
        return HttpResponse(res)
    
@csrf_exempt # include  this
def login(request): #authentication
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        if(len(User.objects.filter(username=username))):
            user=User.objects.filter(username=username)
            if(len(user.filter(password=password))):
                request.session['username']=username # login success then ...
                user_data=User.objects.filter(username=username)
                profile_data=Profile.objects.filter(username=username)
                context={
                    'user_data':user_data,
                    'profile_data':profile_data
                }
                template=loader.get_template("homepage.html")
                res=template.render(context,request)
                return HttpResponse(res)
            else:
                msg='incorrect password.......login again'
                context={
                    'msg':msg
                }
                template=loader.get_template("login.html")
                res=template.render(context,request)
                return HttpResponse(res)
        else:
            msg='incorrect username........login again'
            context={
                'msg':msg
            }
            template=loader.get_template("login.html")
            res=template.render(context,request)
            return HttpResponse(res)
    else:
        template=loader.get_template("login.html")
        res=template.render()
        return HttpResponse(res)

def homepage(request):
    if 'username' not in request.session.keys(): 
        template=loader.get_template("welcome.html")
        res=template.render()
        return HttpResponse(res)
    else:
        username=request.session['username']
        user_data=User.objects.filter(username=username)
        profile_data=Profile.objects.filter(username=username)
        context={   
            'user_data':user_data,
            'profile_data':profile_data
        }
        template=loader.get_template("homepage.html")
        res=template.render(context,request)
        return HttpResponse(res)

def profile(request):
    template=loader.get_template("profile.html")
    res=template.render()
    return HttpResponse(res)

@csrf_exempt # include  this
def profile_save(request):
    if request.method=='POST':
        username=request.session.get('username')
        if(len(User.objects.filter(username=username))):
            profile=Profile() #insertion
            profile.username=User.objects.get(username=username)
            profile.fathers_name=request.POST['father_name']
            profile.mothers_name=request.POST['mother_name']
            profile.phone=request.POST['phone']
            profile.email=request.POST['email']
            profile.address=request.POST['address']
            profile.save()
            user_data=User.objects.filter(username=username)
            profile_data=Profile.objects.filter(username=username)
            context={
                'user_data':user_data,
                'profile_data':profile_data
            }
            template=loader.get_template("homepage.html")
            res=template.render(context,request)
            return HttpResponse(res)
        else:
            msg='incorrect username ,profile not updated'
            context={
                'msg':msg
            }
            template=loader.get_template("profile.html")
            res=template.render(context,request)
            return HttpResponse(res)
    else:
        template=loader.get_template("welcome.html")
        res=template.render()
        return HttpResponse(res)


def logout(request):
    del request.session['username'] #must destroy session keys
    template=loader.get_template("welcome.html")
    res=template.render()
    return HttpResponse(res)

def aboutUs(request):
    template=loader.get_template("about.html")
    res=template.render()
    return HttpResponse(res)


def view_profile(request):
    if 'username' not in request.session.keys(): 
        template=loader.get_template("welcome.html")
        res=template.render()
        return HttpResponse(res)
    else:
        username=request.session['username']
        user_data=User.objects.filter(username=username)
        profile_data=Profile.objects.filter(username=username)
        context={   
            'user_data':user_data,
            'profile_data':profile_data
        }
        template=loader.get_template("view_profile.html")
        res=template.render(context,request)
        return HttpResponse(res)

@csrf_exempt 
def pay(request):
    if request.method == "POST":
        name = request.POST.get('name')
        amount = int(request.POST.get('amount')) * 100  # Razorpay amount is in paise
        #Create Order 
        client = razorpay.Client(auth=("rzp_live_BlFpg6CStP8yfm", "QVxFEhGvT6cmurWYPHKsgyQj"))
        data = { "amount": amount, "currency": "INR", "receipt": "order_rcptid_11" }
        payment = client.order.create(data=data)
        # saving details in out db
        pay = Payment()
        pay.name=name
        pay.amount=amount/100 
        pay.order_id=payment['id']
        pay.save()
        context={
            'payment': payment,
            'name': name
        }
        template=loader.get_template("payment.html")
        res=template.render(context,request)
        return HttpResponse(res)
    template=loader.get_template("pay.html")
    res=template.render()
    return HttpResponse(res)

@csrf_exempt
def success(request):
    if request.method == "POST":
        order_id = request.POST.get("razorpay_order_id", "")
        user = Payment.objects.get(order_id=order_id)
        # optionally we can store these details in our db
        # print(request.POST.get("razorpay_payment_id", ""))
        # print(request.POST.get("razorpay_order_id", ""))
        # print(request.POST.get("razorpay_signature", ""))
        if user:
            user.paid = True
            user.save()
            return render(request, "success.html")
        else:
            context={
                "message": "Order ID not found in the database."
            }
            template=loader.get_template("error.html")
            res=template.render(context,request)
            return HttpResponse(res)
    context={
        "message": "Invalid request method."
    }
    template=loader.get_template("error.html")
    res=template.render(context,request)
    return HttpResponse(res)


def heart(request):
    """
    Lung Cancer Prediction
    """
    # Update the file path to point to the 'data' directory
    file_path = os.path.join(settings.BASE_DIR, 'data', 'LungCancer_train.csv')

    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        # Handle the case where the file is not found
        return HttpResponse("Error: Dataset file not found. Please check the file path.", status=500)

    data = df.values
    X = data[:, :-1]  # Features
    Y = data[:, -1:]  # Target variable (0: No Cancer, 1: Cancer Detected)

    value = ''

    if request.method == 'POST':
        # Replace with lung cancer-related input features
        age = float(request.POST['age'])
        smoking_history = float(request.POST['smoking_history'])
        alcohol_use = float(request.POST['alcohol_use'])
        coughing_duration = float(request.POST['coughing_duration'])
        breathlessness = float(request.POST['breathlessness'])
        chest_pain = float(request.POST['chest_pain'])
        fatigue = float(request.POST['fatigue'])

        # Create input array
        user_data = np.array(
            (age, smoking_history, alcohol_use, coughing_duration, breathlessness, chest_pain, fatigue)
        ).reshape(1, 7)

        # Train Random Forest model
        rf = RandomForestClassifier(n_estimators=20, criterion='gini', max_depth=10)
        rf.fit(np.nan_to_num(X), Y)
        predictions = rf.predict(user_data)

        if int(predictions[0]) == 1:
            value = 'have lung cancer'
        elif int(predictions[0]) == 0:
            value = "don't have lung cancer"

    return render(request,
                  'heart.html',
                  {
                      'context': value,
                      'title': 'Lung Cancer Prediction',
                      'active': 'btn btn-success peach-gradient text-white',
                      'lung_cancer': True,
                      'form': HeartDiseaseForm(),
                  })



# API Key
API_KEY = 'Your_API_Key'

# Configure the Gemini API
ai.configure(api_key=API_KEY)

# Create a new model
model = ai.GenerativeModel("gemini-pro")
chat = model.start_chat()

# Heart Disease Chatbot Logic
def heart_disease_chatbot(user_input):
    user_input = user_input.lower()

    if "heart disease" in user_input or "heart health" in user_input:
        return ("Heart disease refers to various conditions that affect the heart. It can include coronary artery disease, arrhythmias, and heart defects. "
                "It's important to maintain a healthy lifestyle, including a balanced diet and regular exercise.")
    
    elif "symptoms" in user_input:
        return ("Common symptoms of heart disease include chest pain, shortness of breath, fatigue, and irregular heartbeat. "
                "If you experience these symptoms, consult a healthcare professional.")

    elif "causes" in user_input:
        return ("Causes of heart disease can include high blood pressure, high cholesterol, smoking, obesity, and a sedentary lifestyle. "
                "Genetics can also play a role.")

    elif "prevention" in user_input:
        return ("To prevent heart disease, you can maintain a healthy diet, exercise regularly, avoid smoking, limit alcohol intake, "
                "and manage stress levels.")

    elif "diet" in user_input:
        return ("A heart-healthy diet includes fruits, vegetables, whole grains, lean proteins, and healthy fats. "
                "Limit saturated fats, trans fats, and sodium.")

    elif "exercise" in user_input:
        return ("Aim for at least 150 minutes of moderate aerobic exercise per week, such as brisk walking, cycling, or swimming. "
                "Strength training is also beneficial.")

    elif "doctor" in user_input or "consult" in user_input:
        return ("It's important to consult with a healthcare professional for personalized advice and treatment options regarding heart disease.")

    elif "bye" in user_input or "exit" in user_input or "quit" in user_input:
        return "Goodbye! Take care of your heart health!"

    else:
        return None  # If no predefined response, use Gemini API

# View to handle the chatbot interface
def ChatBot(request):
    if request.method == "POST":
        user_input = request.POST.get('user_input')

        # First, check predefined heart disease responses
        response = heart_disease_chatbot(user_input)

        # If no predefined response, call Gemini API
        if response is None:
            gemini_response = chat.send_message(user_input)
            response = gemini_response.text  # Get dynamic response from Gemini API

        return JsonResponse({'response': response})

    return render(request, 'ChatBot.html')

import os
import pandas as pd  # Fake CSV usage
from django.shortcuts import render
from django.http import JsonResponse
from sklearn.ensemble import RandomForestClassifier  # Fake ML model usage
import time  # To simulate training duration
import random  # Fake metrics generation

# Global variables for tracking state
TRAINING_STATUS = False
FAKE_MODEL = RandomForestClassifier()
IMPORTED_FILE = None


def index(request):
    """Render the main HTML page."""
    return render(request, 'index.html')


def import_data(request):
    """Handle file import (simulate loading CSV and image)."""
    global IMPORTED_FILE
    if request.method == "POST":
        IMPORTED_FILE = request.FILES.get('file')
        # Simulate loading CSV
        try:
            df = pd.read_csv("stage1_labels.csv")
        except FileNotFoundError:
            df = pd.DataFrame({"id": ["001", "002"], "cancer": [1, 0]})
        
        return JsonResponse({"message": "File imported successfully."})
    return JsonResponse({"message": "Failed to import file."})


def train_model(request):
    """Simulate model training and return fake metrics."""
    global TRAINING_STATUS
    time.sleep(1)  # Simulating loading

    # Fake metrics
    fake_accuracy = round(random.uniform(85, 99), 2)
    fake_precision = round(random.uniform(80, 95), 2)
    fake_recall = round(random.uniform(75, 90), 2)
    TRAINING_STATUS = True

    return JsonResponse({
        "message": "Model training completed successfully!",
        "accuracy": f"{fake_accuracy}%",
        "precision": f"{fake_precision}%",
        "recall": f"{fake_recall}%"
    })


def predict_model(request):
    """Predict lung cancer based on image name."""
    global IMPORTED_FILE, TRAINING_STATUS

    if not TRAINING_STATUS or not IMPORTED_FILE:
        return JsonResponse({"message": "Please import and train first."})

    # Get file name and simulate prediction
    image_name = str(IMPORTED_FILE).lower()
    cancer_keywords = ["cancer", "tumor", "malignant", "positive", "abnormal"]
    healthy_keywords = ["healthy", "normal", "clear", "negative"]

    if any(keyword in image_name for keyword in cancer_keywords):
        result = "Prediction: The X-ray image indicates possible lung cancer."
    elif any(keyword in image_name for keyword in healthy_keywords):
        result = "Prediction: The X-ray image indicates no lung cancer."
    else:
        result = "Prediction: Unable to determine. Please consult a doctor."

    return JsonResponse({"prediction": result})

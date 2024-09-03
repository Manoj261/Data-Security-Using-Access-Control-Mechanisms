from django.http import HttpResponse
from django.contrib.auth import logout
import joblib
import uuid
from .forms import SignUpForm
from django.conf import settings
import random
from django.core.mail import send_mail
import string
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from .models import Register
from math import sqrt
from .models import LOTP
from .forms import SignInForm
from django.contrib import messages
import os
import pandas as pd
from django.utils import timezone
from datetime import timedelta
from .forms import ProfileForm
from .models import Profile
from .encyption import encrypt
from .encyption import decrypt
from .models import Predict
from .models import Register, Profile# Role

from datetime import datetime, date
#import joblib
#from .....aesencryption import *
key = os.urandom(32)
def message_testing(request):
     messages.success(request,"this is a success")
     return HttpResponse("<h1>Valid</h1>")

def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

def generate_otp4():
    return ''.join(random.choices(string.digits, k=4))

def generate_otp8():
    return ''.join(random.choices(string.digits, k=8))

def mahiValid(s_otp,e_otp):
     return s_otp==e_otp + 2*(sqrt(0.5))

def cheap(request):
    return HttpResponse("<h1>Default Route</h1>")

def login(request):
    return render(request,"LOGIN_OTP.html")

def model(request):
     return render(request,"predict.html")

def home(request):
    return render(request, "ss.html")
def get_last_row():
    try:
        last_row = Register.objects.last()
        return last_row
    except Register.DoesNotExist:
        return None
def send_otp_email(request):
    email = request.session.get('email')

    otp = request.session.get('otp')

    if email and otp:
        subject = 'Your OTP for Registration'

        message = f'Your OTP is: {otp}'

        email_from = settings.EMAIL_HOST_USER

        recipient_list = [email]

        send_mail(subject, message, email_from, recipient_list)
    else:
        print("Email or OTP not found in session.")

def sendmail(request):
    pass

def signup(request):  
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        #form1 = ProfileForm(request.POST)
        if form.is_valid():
            try:
                username = form.cleaned_data['username']

                email = form.cleaned_data['email']

                password = form.cleaned_data['password']  
                
                #password=encrypt_message("quwjdweyfwrfu^2282Hu289",password)
                #password=encrypt(key,password)
                
                otp = generate_otp()
                print(otp)
                request.session['otp'] = otp

                request.session['usernmame'] = username
                request.session['email'] = email
                print(request.session)
                send_mail(
                    'Validate Form',  
                    f'Your OTP is: {otp}',
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False
                )  

                Register.objects.create(username=username, email=email, password=password,role='user')
                
                print("Data saved successfully to the database.")
                
                Profile.objects.create(username=username,email=email,location="",bio="")
                
                print("Profile also updated!");
                messages.success(request,"OTP Sent Successfully")
                
                return render(request, 'REGISTER_OTP.html')
              
            except Exception as e:
                print(f"Error occurred while saving data: {e}")
                return render(request, 'error.html', {'error_message': 'An error occurred while saving data. Please try again.'})
        else:
            print("Form is not valid. Errors:", form.errors)
            return render(request,'ss.html');
    else:
        form = SignUpForm()
        return HttpResponse("<h1>Hello</h1>")
def get_first_row_with_otp():
    try:
        first_row_with_otp = Register.objects.filter(otp__isnull=False).first()
        if first_row_with_otp:
            return first_row_with_otp.otp
        else:
            return None  
    except Exception as e:
        print(f"Error occurred while retrieving the first row with OTP: {e}")
        return None  
def get_last_row_login():
    try:
        last_row = LOTP.objects.last()
        return last_row
    except LOTP.DoesNotExist:
        return None
def verify_otp(request):
    if request.method == 'POST':
        otp_entered=''
        if request.method == 'POST':
            otp_entered+=(request.POST.get('gg1',''))
            otp_entered+=(request.POST.get('gg2',''))
            otp_entered+=(request.POST.get('gg3',''))
            otp_entered+=(request.POST.get('gg4',''))
            otp_entered+=(request.POST.get('gg5',''))
            otp_entered+=(request.POST.get('gg6',''))

            stored_otp = request.session.get('otp')

            print("stored",stored_otp,"entered",otp_entered)
           
            if otp_entered == stored_otp:
                #request.session.flush()
                return redirect("/")
            
            else:
                return HttpResponse("Invalid OTP. Please try again.")
        else:
            return HttpResponse("User not found.")
    else:
        return HttpResponse("Method not allowed.")

global N
N = 4

def printSolution(board):
	for i in range(N):
		for j in range(N):
			print (board[i][j],end=' ')
		print()
          

def isSafe(board, row, col):
	for i in range(col):
		if board[row][i] == 1:
			return False
	for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
		if board[i][j] == 1:
			return False
	for i, j in zip(range(row, N, 1), range(col, -1, -1)):
		if board[i][j] == 1:
			return False

	return True

def solveNQUtil(board, col):
	if col >= N:
		return True
	for i in range(N):
		if isSafe(board, i, col):
			board[i][col] = 1
			if solveNQUtil(board, col + 1) == True:
				return True
			board[i][col] = 0
	return False

def signin1(request):
    if request.method == 'POST':
        signin_username = request.POST.get('signin_username') 
        signin_password = request.POST.get('signin_password')
        try:
            user = Register.objects.get(username=signin_username)
        except Register.DoesNotExist:
           
            return render(request, 'Mahesh.html', {'signin_error': 'Invalid username or password'})
        login(request, user)
        return redirect('home')  
           
        #return render(request, 'Mahesh.html', {'signin_error': 'Invalid username or password'})

    else:
        return render(request, 'Mahesh.html')
    
def predictions(request):
     return render(request,"predict.html")

def signin(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        signin_username = request.POST.get('signin_username') 
        signin_password = request.POST.get('signin_password')
        #try:
        user = Register.objects.get(username=signin_username)

        users = Register.objects.all()

        print(user.role)
        if user.role == 'admin':
             return render(request,"Admin.html",{'users':users})

        password=user.password
        # except Register.DoesNotExist:
        #     return render(request, 'Mahesh.html', {'signin_error': 'Invalid username or password'})
        if password == signin_password:
            otp = generate_otp4()
            request.session['otp']=otp
            request.session['otp_timestamp'] = timezone.now().isoformat()
            request.session['username'] = user.username
            print(user.username)
            print(otp)
            
            send_mail(
                 'Validate Form',  
                    f'Your OTP is: {otp}',
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False
            )
            #otp_log = LOTP.objects.create(otpL=otp,username=signin_username)
            return render(request,'LOGIN_OTP.html')
        else:
            return render(request,"ss.html")
    else:
        return HttpResponse("<h1>request is not post<h1>")
    

def admin1(request):
     all_users = Register.objects.all()

     return render(request,'Admin.html',{'users':all_users})


def delete_user(request,username):
        
     
        user = Register.objects.get(username=username)


        user.delete()

        mm = Profile.objects.get(username=username)

        mm.delete()

        return redirect('admin1')
    

          
    
def lvf(request):
     if request.method == 'POST':
          otp_entered=''
          if request.method == 'POST':

            
            otp_entered+=(request.POST.get('otp1',''))
            otp_entered+=(request.POST.get('otp2',''))
            otp_entered+=(request.POST.get('otp3',''))
            otp_entered+=(request.POST.get('otp4',''))

            stored_otp = request.session.get('otp')
            #print('hi')
            print("stored",stored_otp,"entered",otp_entered)
           
            if otp_entered == stored_otp:
                messages.success(request, "OTP Verified Successfully.")
                return redirect("profile")
                #                 "profile.html"
                #                 )
                # #may be
                # # cant reach
                #return HttpResponse("OYO didnt match")
            else:
                return HttpResponse("not match")


def logout_view_secc(request):
     logout(request)
     return redirect("/")


def profile(request):

    username=request.session.get('username')
    
    print(username)
    
    try:
        profile = Profile.objects.get(username=username)
        predictions = Predict.objects.filter(username=username)
        print("PPProfile:",profile)
    except Profile.DoesNotExist:
        profile = None

    return render(request, 'profile.html', {'profile': profile,'predictions':predictions})

def hot(request):
    return render(request,'sample.html')



def submit(request):
     print(request.method)
     if request.method =='POST':
          print("debug")
          gmail=request.session.get('email')
          message=request.POST.get('sentence')
          send_mail(
                    'Validate Form',  
                    f'Your msg is: {message} ',
                    settings.EMAIL_HOST_USER,
                    [gmail],
                    fail_silently=False
                ) 
          return redirect("profile")
     else:
          return HttpResponse("Not valid")


def resend_otp(request):
    otp = generate_otp4()
    request.session['otp'] = otp
    request.session['otp_timestamp'] = timezone.now().isoformat()
    send_otp_email(request.user.email, otp)
    return redirect('signin')



def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()




# class Crop:
#     def __init__(self, file_path):
#         self.file_path = file_path
#         self.data = None
#         self.label_encoder = LabelEncoder()
#         self.rf_classifier = RandomForestClassifier(random_state=42)
#         self.X_train = None
#         self.X_test = None
#         self.y_train = None
#         self.y_test = None

#     def load_data(self):
#         self.data = pd.read_csv(self.file_path)
#         self.data['label'] = self.label_encoder.fit_transform(self.data['label'])

#     def preprocess_data(self):
#         X = self.data.drop(columns=['label'])
#         y = self.data['label']
#         self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#     def train_model(self):
#         self.rf_classifier.fit(self.X_train, self.y_train)

#     def evaluate_model(self):
#         y_pred = self.rf_classifier.predict(self.X_test)
#         accuracy = accuracy_score(self.y_test, y_pred)
#         report = classification_report(self.y_test, y_pred, target_names=self.label_encoder.classes_)
#         print(f'Accuracy: {accuracy}')
#         print('Classification Report:')
#         print(report)

#     def save_model(self, model_path, encoder_path):
#         joblib.dump(self.rf_classifier, model_path)
#         joblib.dump(self.label_encoder, encoder_path)

# if __name__ == "__main__":
#     file_path = 'C:\Users\Admin\OneDrive\Documents\Crop_recommendation.csv'
#     model_path = 'rf_crop_model.pkl'
#     encoder_path = 'label_encoder.pkl'

#     crop_model = Crop(file_path)
#     crop_model.load_data()
#     crop_model.preprocess_data()
#     crop_model.train_model()
#     crop_model.evaluate_model()
#     crop_model.save_model(model_path, encoder_path)

def sample_text(request):
     return render(request,"sample.html")


def predict(request):
     if request.method == 'POST':
            N = float(request.POST['N'])
            P = float(request.POST['P'])
            K = float(request.POST['K'])
            temperature = float(request.POST['temperature'])
            humidity = float(request.POST['humidity'])
            ph = float(request.POST['ph'])
            rainfall = float(request.POST['rainfall'])

            input_data = [[N, P, K, temperature, humidity, ph, rainfall]]
            feature_names = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
            new_data_df = pd.DataFrame(input_data, columns=feature_names)

            rf_classifier = joblib.load('rf_crop_model.pkl')
            label_encoder = joblib.load('label_encoder.pkl')

            predictions = rf_classifier.predict(new_data_df)
            predicted_labels = label_encoder.inverse_transform(predictions)


            username=request.session.get("username")
            Predict.objects.create(username=username,N=N,temp=temperature,rainfall=rainfall,jathak=predicted_labels[0],timesytamp=datetime.now())

            print("data saved to predictions!")

            #print('Predicted crop types:', predicted_labels)

            return redirect("profile")
     else:
          return HttpResponse('No form is invalid')

# def manage_users(request):
#     if not request.user.role.name == 'Admin':
#         return HttpResponse("You are not authorized to view this page.")

#     users = Register.objects.all()
#     roles = Role.objects.all()

#     if request.method == 'POST':
#         user_id = request.POST.get('user_id')
#         new_role_id = request.POST.get('role_id')
#         user = Register.objects.get(username=user_id)
#         new_role = Role.objects.get(id=new_role_id)
#         user.role = new_role
#         user.save()
#         return redirect('manage_users')

#     return render(request, 'manage_users.html', {'users': users, 'roles': roles})
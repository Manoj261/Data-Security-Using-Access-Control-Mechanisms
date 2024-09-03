
from django import forms
from .models import Register
from .models import LOTP
from .models import Profile
from .models import Predict
class SignUpForm(forms.ModelForm):
    class Meta:
        model = Register
        db_table = 'register'
        fields = [
            'username',
              'email',
              'password'
            ]
class SignInForm(forms.ModelForm):
    class Meta:
        model = LOTP
        db_table = 'LOTP'
        fields = [
            'otpL','username'
            ]



        
class ProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        db_table='profile'
        fields=[
            'username',
            'bio',
            'location',
            'email'
        ]



class PredictionForm(forms.ModelForm):
    class Meta:
        model=Predict
        db_table="predict"
        fields=[
            'username',
            'N',
            'temp',
            "rainfall"
            ,
            'jathak'

        ,
        'timesytamp'
        ]

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from .models import CustomUser, Quote

class CustomUserCreationForm(UserCreationForm):
    class Meta: 
        model = CustomUser
        fields = ['email', 'full_name', 'phone_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True


class CustomUserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    user = None

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if user is None:
                raise forms.ValidationError("Invalid email or password")
            if not user.is_active:
                raise forms.ValidationError("This account is inactive")
            self.user = user

        return cleaned_data

    def get_user(self):
        return self.user
    

class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = [ 
            'full_name', 'business_name', 'email', 'phone_number', 'project_details', 'address', 'unit',
            'city', 'province', 'postal_code', 'property_type', 'preferred_date', 'preferred_time'
        ]
        widgets = {
            'preferred_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'preferred_time': forms.Select(attrs={'class': 'form-control'}),
            'project_details': forms.Textarea(attrs={
                'rows': 4, 'placeholder': 'Please provide as much info as possible...'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            if field.required:
                field.label_suffix = ' *'  # adds asterisk to required fields
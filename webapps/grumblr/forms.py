from django import forms
from django.contrib.auth.forms import AuthenticationForm

from grumblr.models import *


class RegistrationForm(forms.Form):
	username = forms.CharField(label='Username', max_length=20, widget=forms.TextInput(attrs={'class': 'form-control' , 'placeholder': 'Username'}))
	email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control' , 'placeholder': 'Email'}))
	password1 = forms.CharField(label='Password', max_length=200, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
	password2 = forms.CharField(label='Confirm password',  max_length=200, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password Confirm'}))
	firstname = forms.CharField(label='Firstname', max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Firstname'}))
	lastname = forms.CharField(label='Lastname', max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lastname'}))
	age = forms.IntegerField(label='Age', validators=[MaxValueValidator(200), MinValueValidator(0)], widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Age'}))
	bio = forms.CharField(label='Short Bio', max_length=420, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': '420 characters or less'}))

	def clean(self):
		cleaned_data = super(RegistrationForm, self).clean()

		password1 = cleaned_data.get('password1')
		password2 = cleaned_data.get('password2')

		if password1 != password2:
			raise forms.ValidationError("Passwords did not match.")
		return cleaned_data

	def clean_username(self):
		username = self.cleaned_data.get('username')
		if User.objects.filter(username__exact=username):
			raise forms.ValidationError("Username has already token.")
		return username


class LoginForm(AuthenticationForm):
	username = forms.CharField(label='Username', max_length=20, widget=forms.TextInput(attrs={'class': 'form-control' , 'placeholder': 'Username'}))
	password = forms.CharField(label='Password', max_length=200, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

	def clean_username(self):
		username = self.cleaned_data.get('username')
		return username


class UserForm(forms.ModelForm):

	class Meta:
		model = User
		fields = ('first_name','last_name')
		widgets = {'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Firstname'}),
			   'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lastname'})}


class ProfileForm(forms.ModelForm):

	class Meta:
		model = Profile
		fields = ('age', 'bio', 'avatar')
		widgets = {'age' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Age'}),
			   'bio' : forms.Textarea(attrs={'class': 'form-control', 'placeholder': '420 characters or less'}),
			'avatar': forms.FileInput()}


class ChangePasswordForm(forms.Form):
	oldpassword = forms.CharField(label='Old Password', max_length=200, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Old Password'}))
	new_password = forms.CharField(label='New Password', max_length=200, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password'}))
	confirm_password = forms.CharField(label='Confirm Password', max_length=200, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Password Confirm'}))

	def clean(self):
		cleaned_data = super(ChangePasswordForm, self).clean()

		password1 = cleaned_data.get('new_password')
		password2 = cleaned_data.get('confirm_password')

		if password1 != password2:
			raise forms.ValidationError("New Passwords did not match.")
		return cleaned_data


class ResetPasswordForm(forms.Form):
	email = forms.EmailField(label='Email',
				 widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))

	def clean(self):
		cleaned_data = super(ResetPasswordForm, self).clean()
		email = cleaned_data.get('email')

		if not User.objects.filter(email__exact=email):
			raise forms.ValidationError("Email address is not registered")
		return cleaned_data


class ResetForm(forms.Form):
	new_password = forms.CharField(label='New Password', max_length=200, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password'}))
	confirm_password = forms.CharField(label='Confirm Password', max_length=200, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Password Confirm'}))

	def clean(self):
		cleaned_data = super(ResetForm, self).clean()

		password1 = cleaned_data.get('new_password')
		password2 = cleaned_data.get('confirm_password')

		if password1 != password2:
			raise forms.ValidationError("New Passwords did not match.")
		return cleaned_data


class PostForm(forms.Form):
	post = forms.CharField( max_length=42, widget=forms.Textarea(
		attrs={'class': 'form-control', 'id': 'post-field', 'placeholder': 'No more than 42 characters'}))

	def clean(self):
		cleaned_data = super(PostForm, self).clean()
		return cleaned_data


class CommentForm(forms.Form):
	comment = forms.CharField(max_length=42, widget=forms.TextInput(
		attrs={'class': 'form-control', 'placeholder': 'Add comment'}))

	def clean(self):
		cleaned_data = super(CommentForm, self).clean()
		return cleaned_data
from django import forms
from models import Group
from models import Profile
from models import Business
from models import Message

from django.contrib.auth.models import User


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=20, label='User name',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'User name'}))
    first_name = forms.CharField(max_length=20, label='First name',
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}))
    last_name = forms.CharField(max_length=20, label='Last name',
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}))
    email1 = forms.CharField(max_length=100, label='Email',
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password1 = forms.CharField(max_length=20, label='Password',
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(max_length=20, label='Confirm password',
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control', 'placeholder': 'Confirm password'}
                                ))

    def clean(self):

        cleaned_data = super(RegistrationForm, self).clean()

        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        return cleaned_data

    def clean_username(self):

        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")

        return username
    pass


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', 'follower', 'password')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Age'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Bio'}),
            'picture': forms.FileInput(attrs={'class': 'form-control'}),
            'password': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        }
        pass


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'lat', 'lon', 'radius', 'lifetime', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Group Name'}),
            'lat': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Group Latitude'}),
            'lon': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Group Longitude'}),
            'radius': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Group Radius in Meters'}),
            'lifetime': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Group Lifetime in Hours'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Group Description'})
        }
        pass

    def clean_name(self):
        cleaned_data = super(GroupForm, self).clean()
        name = cleaned_data.get('name')
        groups = Group.objects.filter(name=name)
        if len(groups) > 0:
            raise forms.ValidationError('duplicate group name')
        return name

    def clean_lat(self):
        cleaned_data = super(GroupForm, self).clean()
        lat = cleaned_data.get('lat')
        if lat < -90 or lat > 90:
            raise forms.ValidationError('invalid latitude')
        return lat

    def clean_lon(self):
        cleaned_data = super(GroupForm, self).clean()
        lon = cleaned_data.get('lon')
        if lon < -180 or lon > 180:
            raise forms.ValidationError('invalid longitude')
        return lon

    def clean_radius(self):
        cleaned_data = super(GroupForm, self).clean()
        radius = cleaned_data.get('radius')
        if radius < 50 or radius > 200:
            raise forms.ValidationError('radius should be 50 - 200 meters')
        return radius

    def clean_lifetime(self):
        cleaned_data = super(GroupForm, self).clean()
        lifetime = cleaned_data.get('lifetime')
        if lifetime < 1 or lifetime > 24:
            raise forms.ValidationError('lifetime should be 1 - 24 hours')
        return lifetime
    pass


class LatLonForm(forms.Form):
    lat = forms.FloatField()
    lon = forms.FloatField()

    def clean_lat(self):
        cleaned_data = super(LatLonForm, self).clean()
        lat = cleaned_data.get('lat')
        if lat < -90 or lat > 90:
            raise forms.ValidationError('invalid latitude')
        return lat

    def clean_lon(self):
        cleaned_data = super(LatLonForm, self).clean()
        lon = cleaned_data.get('lon')
        if lon < -180 or lon > 180:
            raise forms.ValidationError('invalid longitude')
        return lon
    pass


class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ['name', 'categories', 'lat', 'lon', 'is_closed', 'image_url',
                  'url', 'display_phone', 'review_count', 'rating']
        pass
    pass


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        pass
    pass


class SearchForm(forms.Form):
    type = forms.ChoiceField(choices=[('group', 'group'), ('business', 'business'), ('user', 'user')])
    method = forms.ChoiceField(choices=[('keyword', 'keyword'), ('location', 'location')])
    keyword = forms.CharField(max_length=100, required=False)
    lat = forms.FloatField(required=False, max_value=90, min_value=-90)
    lon = forms.FloatField(required=False, max_value=180, min_value=-180)
    radius = forms.FloatField(required=False, max_value=1000, min_value=100)

    def clean(self):
        cleaned_data = super(SearchForm, self).clean()
        if cleaned_data.get('type') == 'user' and cleaned_data.get('method') != 'keyword':
            raise forms.ValidationError('You can only search users with keyword.')
        if cleaned_data.get('method') == 'keyword' and (
                        'keyword' not in cleaned_data or not cleaned_data.get('keyword')):
            raise forms.ValidationError('Keywords must be provided in keyword search.')
        if cleaned_data.get('method') == 'location' and (
                'lat' not in cleaned_data or cleaned_data.get('lat') is None or
                'lon' not in cleaned_data or cleaned_data.get('lon') is None or
                'radius' not in cleaned_data or cleaned_data.get('radius') is None):
            raise forms.ValidationError('Latitude, longitude and radius must be provided in location search.')
        return cleaned_data
    pass

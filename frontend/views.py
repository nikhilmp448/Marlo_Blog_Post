import requests
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages , auth
# Create your views here.


# this login page control if the user is entering redirect to user side or else goes to adminside
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # Make a POST request to the external API
        api_url = 'http://127.0.0.1:8000/api/user/login/'
        api_data = {'email': email, 'password': password}
        response = requests.post(api_url, data=api_data)

        if response.status_code == 200 :
            user = authenticate(request, email=email, password=password)
            if user is not None:
                auth.login(request,user)
                if user.is_staff == False:
                    return redirect('blog-post-list')  # Redirect to a dashboard page after login
                else:
                    return redirect('admin')
            else:
                return render(request, 'login.html', {'error_message': 'Authentication failed'})
        else:
            return render(request, 'login.html', {'error_message': 'Invalid username or password'})
    return render(request,'login.html')

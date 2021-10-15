from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import MachineForm
from .models import Machine, Part, Log
import csv

@login_required(login_url='/login')
def home(request):
    return render(request, "home.html", {})

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Set a success message
            messages.success(request, ("Logged In Successfully"))
            # Redirect to the homepage
            return redirect('home')
        else:
            # Set an error message
            messages.success(request, ("Invalid Login Credentials"))
            return redirect('login')
    else:
        return render(request, "login.html", {})

def user_logout(request):
    logout(request)
    # Set a success message
    messages.success(request, ("Logged Out Successfully"))
    # Redirect to the homepage
    return redirect('login')

@login_required(login_url='/login')
def machines(request):

    # Handle the creation of a new machine
    if request.method == 'POST':
        filled_form = MachineForm(request.POST)

        # Check if the machine is already registered
        machine_exists = Machine.objects.filter(description=request.POST.get('description'))
        if machine_exists:
            messages.success(request, ("The machine is already registered"))
            # Render the page with the datatabase entries and a new form
            all_machines = Machine.objects.all()
            create_machine_form = MachineForm()
            return render(request, "machines.html", {"all_machines" : all_machines, "create_machine_form" : create_machine_form})

        # Machine is not registered
        else:
            # Check if the form is valid
            if filled_form.is_valid():
                filled_form.save()

                # Set a success message
                messages.success(request, ("New machine created"))

                # Render the page with the datatabase entries and a new form
                all_machines = Machine.objects.all()
                create_machine_form = MachineForm()
                return render(request, "machines.html", {"all_machines" : all_machines, "create_machine_form" : create_machine_form})
    
    else:
        # Render the page with the datatabase entries and a new form
        all_machines = Machine.objects.all()
        create_machine_form = MachineForm()
        return render(request, "machines.html", {"all_machines" : all_machines, "create_machine_form" : create_machine_form})

@login_required(login_url='/login')
def delete_machine(request, id):
    machine = Machine.objects.get(pk=id)
    machine.delete()
    messages.success(request, ("Machine Deleted"))
    return redirect('machines')

@login_required(login_url='/login')
def parts(request):
    # Render the page with all database entries
    all_parts = Part.objects.all()
    return render(request, "parts.html", {"all_parts": all_parts})


@login_required(login_url='/login')
def download_log(request, id):
    # Define the response format
    response = HttpResponse(content_type='text/csv')
    # Define the csv writer and column format
    writer = csv.writer(response)
    writer.writerow(['Temperature', 'Humidity', 'Volume'])

    # Query the part
    logged_part = Part.objects.get(pk=id)

    for log in Log.objects.filter(part=logged_part).values_list('temperature', 'humidity', 'volume'):
        writer.writerow(log)

    response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(logged_part.description)

    return response

@login_required(login_url='/login')
def delete_part(request, id):
    part = Part.objects.get(pk=id)
    part.delete()
    messages.success(request, ("Part Deleted"))
    return redirect('parts')
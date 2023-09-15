from django.db.models import Q
from tablib import Dataset
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from user_proj import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
# from django.utils.encoding import force_text
# from . tokens import generate_token
# from .resources import employeeResource
from django.core.mail import EmailMessage,send_mail
from .models import employee
# Create your views here.


def home(request):
    return render(request,'home.html')


def index(request):
    return render (request,'index.html')


def view_all(request):
    emps = employee.objects.all()
    context={
        'emps':emps
    }
    print(context)
    return render(request,'view_all.html',context)



def sign_up(request):
    if request.method == 'POST':
        username=request.POST['username']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']

        if User.objects.filter(username=username):
            messages.error(request,'Account already exist Please check Your username')
            return redirect('home')


        if User.objects.filter(email=email):
            messages.error(request,'Account already exist Please check Your Email ID')    
            return redirect('home')
        
        # if username>25:
        #     messages.error(request,'Your username should be under 25 characters')

        if password!=confirm_password:
            messages.error(request,'Password didn"t match')

        if not username.isalnum():
            messages.error(request,'username should be alphanumeric')    
            return redirect('home')

        new_user=User.objects.create_user(username,email,password)
        new_user.first_name=first_name
        new_user.last_name=last_name
        new_user.is_active=False
        new_user.save()
        
        messages.success(request,'Your Account has been succesfully created!') 
                        #  we have sent you confirmation email to account')

        # #welcome eMAIL
        # subject='WELCOME TO DJANGO'
        # message='hello',new_user.first_name+"\n",'welcome to Django Project\n','thank you\n'
        # from_email=settings.EMAIL_HOST_USER
        # to_list=[new_user.email]
        # send_mail(subject,message,from_email,to_list,fail_silently=True)


        # Email Addresss
        # current_site=get_current_site(request)
        # email_subject='Confirm Your Email'
        # message2=render_to_string('email_confirmation.html',
        #                           {'name':new_user.first_name,
                                                               
        #                         'domain':current_site.domain,
        #                     'uid':urlsafe_base64_encode(force_bytes(new_user.pk)),
        #                     'token':generate_token.make_token(new_user)})
        
        # email=EmailMessage(email_subject,current_site,message2,settings.EMAIL_HOST_USER,
        #                    [new_user.email])
        # email.fail_silently=True
        # email.send()



        return redirect('sign_in')

    return render(request,'sign_up.html')

def add_emp(request):
    if request.method == 'POST':
        PIN = request.POST['PIN']
        full_name = request.POST['full_name']
        Primary_PhoneNum = int(request.POST['Primary_PhoneNum'])
        Alternative_Phonenum = int(request.POST['Alternative_Phonenum'])
        Email_Id = request.POST['Email_Id']
        profession = request.POST['profession']
        Location=request.POST['Location']
        
        
        
        new_emp= employee(PIN=PIN,full_name=full_name,Primary_PhoneNum=Primary_PhoneNum,Alternative_Phonenum = Alternative_Phonenum,Email_Id=Email_Id,profession=profession,Location=Location)
        new_emp.save()
        return HttpResponse('Employee Added Sucessfully')
    elif request.method=='GET':
        return render(request,'add_emp.html')
    else:
        return HttpResponse('An error Occured! Member is not added to the list')

def BackBtn(request):
    return render(request,'back.html')        



def activate(request,uidb64,token):
    try:
        uid=force_str(urlsafe_base64_decode(uidb64))
        new_user=User.objects.get(pk=uid)
    except(ValueError,TypeError,OverflowError,User.DoesNotExist):
        new_user=None
    # if new_user is not None and generate_token.check_token(new_user,token):
        new_user.is_active=True
        new_user.save()
        login(request,new_user)
        return redirect('home')
    else:
        return render(request,'activation_failed.html')
    




def sign_in(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        user = authenticate(username=username,password=password)

        if user is not None:
            # first_name=user.first_name
            login(request,user)
            messages.success(request,f'{username} you have sucessfully logged In')
            return render(request,'index.html')




        else:
            messages.error(request,'Bad credentials!')
            return redirect('sign_up')    

    return render(request,'sign_in.html')



def sign_out(request):
    logout(request)
    messages.success(request,'logged Out Sucessfully')
    return redirect('home')
    # return render(request,'sign_out.html')


def update(request,emp_PIN):
    emp=employee.objects.get(PIN=emp_PIN)

    return render(request,'update.html',{'emp':emp})

def do_update(request,emp_PIN):

    PIN=request.POST.get('PIN')
    full_name = request.POST.get('full_name')
    Primary_PhoneNum = request.POST.get('Primary_PhoneNum')
    Alternative_Phonenum = request.POST.get('Alternative_Phonenum')
    Email_Id = request.POST.get('Email_Id')
    profession = request.POST.get('profession')
    Location=request.POST.get('Location')

    # emp=employee.objects.get(PIN=emp_PIN)
    emp = employee.objects.get(PIN=emp_PIN)

    emp.PIN=PIN
    emp.full_name=full_name
    emp.Primary_PhoneNum=Primary_PhoneNum
    emp.Alternative_Phonenum=Alternative_Phonenum
    emp.Email_Id=Email_Id
    emp.profession=profession
    emp.Location=Location

    emp.save()
    return redirect('/view_all')    


def remove(request,emp_PIN=0):
    if emp_PIN:
        try:
            emp_to_be_removed=employee.objects.get(PIN=emp_PIN)
            emp_to_be_removed.delete()
            return HttpResponse('Member has been removed SucessFully')
        except:
            return HttpResponse('Please Enter Proper Emp_Id')
    emps = employee.objects.all()
    context = {
        'emps':emps
    }
    return render(request,'remove.html',context)   


def delete_all(request,emp_PIN=0):
    emp_to_be_deleted=employee.objects.get(PIN=emp_PIN)
    if request.method == 'POST':
        emp_to_be_deleted.delete()
        return redirect('/view_all')
   
    return render(request,'delete.html')

def filter_emp(request):
    if request.method=='POST':
        search = request.POST['search']
        emps=employee.objects.all()
        
        if search:
            emps = emps.filter(Q(full_name__icontains= search)| Q(Primary_PhoneNum__icontains =search)
                               |Q(Alternative_Phonenum__icontains=search)|Q(Email_Id__icontains =search)
                               |Q(profession__icontains =search)|Q(Location__icontains =search))
            context={
            'emps':emps
        }    
        return render(request,'view_all.html',context)
    else:
        return HttpResponse('Member has not been added')

    return render(request,'filter_emp.html')





def upload(request):
    if request.method == 'POST':
        # EmployeeResource = employeeResource()
        dataset=Dataset()
        New_employee=request.FILES['myfiles']
        imported_data= dataset.load(New_employee.read(),format='xlsx')
        try:
            for data in imported_data:
                value = employee(
                    data[0],
                    data[1],
                    data[2],
                    data[3],
                    data[4],
                    data[5], 
                    data[6],
                    data[7],)
                value.save()
            return HttpResponse('Excel file has been uploaded Sucessfully')
        except:
            return HttpResponse('Invalid Format! Please Check the Table Format')   
    return render(request,'upload.html')
   
   

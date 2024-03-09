from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from authentication.models import user, travel_agency, admin, Verified_travel_agency, schedule, ticket
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import os
from django.core.mail import EmailMultiAlternatives
import random
import razorpay
from smtplib import SMTPException
from django.core.mail import send_mail
from os import path
from datetime import datetime


@login_required(login_url='login')
def home(request):
    showdata = request.session['um']

    if request.method == "POST":

        if request.POST.get('form') and request.POST.get('optradio') and request.POST.get('to') and request.POST.get(
                'date') and request.POST.get('time') and request.POST.get('date') and request.POST.get(
                'total_seat') and request.POST.get('date') and request.POST.get('window') and request.POST.get(
                'date') and request.POST.get('general') and request.POST.get('date') and request.POST.get(
                'price') and request.POST.get('date') and request.POST.get('bus_number'):
            saveschedule = schedule()
            st = Verified_travel_agency.objects.get(id=request.session['um'])
            print(request.POST.get('optradio'))
            saveschedule.form = request.POST.get('form')
            saveschedule.date = request.POST.get('date')
            saveschedule.time = request.POST.get('time')
            saveschedule.to = request.POST.get('to')
            saveschedule.bus_number = request.POST.get('bus_number')
            saveschedule.bus_type = request.POST.get('optradio')
            saveschedule.price = request.POST.get('price')
            saveschedule.total_seats = request.POST.get('total_seat')
            saveschedule.window = request.POST.get('window')
            saveschedule.general = request.POST.get('general')
            saveschedule.agency_number = request.session['um']
            saveschedule.agency_name = st.agency_name
            saveschedule.pk = request.session['um'] + request.POST.get('bus_number')
            messages.success(request, "schedule successfully added")
            total = int(request.POST.get('total_seat'))
            window = int(request.POST.get('window'))
            general = int(request.POST.get('general'))
            if total == window + general:
                try:
                    saveschedule.save()
                    messages.success(request, "schedule successfully added")
                except:
                    messages.error(request, "please enter valid data")
            else:
                messages.error(request, "please enter valid data")

    print(showdata)

    return render(request, 'set_schedule.html', {'data': showdata})


@login_required(login_url='adhome')
def adhome(request):
    showem = travel_agency.objects.all()
    return render(request, 'fetch_travel_agency_details.html', {'data': showem})


def Logoutpage(request):
    logout(request)
    return redirect('login')


def loginpage(request):
    if request.method == "POST":
        uname = request.POST.get('email')

        pass1 = request.POST.get('password')
        users = user.objects.all()
        print(uname)
        print(pass1)
        tv = Verified_travel_agency.objects.all()
        authadmin = admin.objects.all()
        print(authadmin)
        userauth = authenticate(request, username=uname, password=pass1)
        print(userauth)
        if userauth is not None:

            for au in authadmin:
                if au.mobile_no == uname:
                    login(request, userauth)
                    return redirect('adhome')
            for v in tv:
                if v.mobile_no == uname:
                    request.session['um'] = v.mobile_no
                    print(request.session['um'])
                    login(request, userauth)
                    return render(request, "set_schedule.html")
                    break
            for s in users:
                if s.mobile_no == uname:
                    request.session['um'] = s.mobile_no
                    login(request, userauth)
                    return redirect('user_home')

        else:
            messages.error(
                request, "user name or password is worng.if you do not register,then first register and then login")
            return redirect('login')
    return render(request, 'login.html')


def history(request):
    try:
        showschedule = schedule.objects.all()
        print(datetime.now())
        x = datetime.now()
        v = x.date()
        print(v)
        for d in showschedule:
            if v > d.date:
                d.delete()
            if d.agency_number == request.session['um']:
                mobile = request.session['um']
        print(mobile)
        return render(request, 'history.html', {'data': showschedule, 'number': mobile})
    except Exception as e:
        messages.error(request, str(e))
        return render(request, 'history.html')


def signup(request):
    if request.method == "POST":
        pass1 = request.POST.get('password')
        pass2 = request.POST.get('password1')
        if request.POST.get('tname') and request.POST.get('phone') and request.POST.get('address') and request.POST.get(
                'aadharno') and request.POST.get('password'):
            if pass1 != pass2:
                messages.warning(
                    request, "your password and confirm password are not same")
                return render(request, "registration.html",
                              {"tname": request.POST.get('tname'), "phone": request.POST.get("phone"),
                               "email": request.POST.get("email"), "address": request.POST.get("address"),
                               "anumber": request.POST.get("aadharno"), "file": request.POST.get('file'), })
            else:
                try:
                    saverecord = travel_agency()
                    saverecord.agency_name = request.POST.get('tname')
                    saverecord.pk = request.POST.get('phone')
                    saverecord.mobile_no = request.POST.get('phone')
                    saverecord.address = request.POST.get('address')
                    saverecord.aadhar_no = request.POST.get('aadharno')
                    saverecord.password = request.POST.get('password')
                    saverecord.email = request.POST.get('email')
                    em = request.POST.get('email')
                    saverecord.status = False
                    saverecord.file = "/static/file/" + \
                                      request.FILES['file'].name
                    print(request.FILES)
                    handle_uploaded_file(request.FILES['file'])

                    saverecord.save()
                    print(saverecord.save())
                    if saverecord.save():

                        messages.success(
                            request, 'Travel Agency ' + saverecord.agency_name + ' details are saved suceessfully..!')
                        if messages.success:
                            my_user = User.objects.create_user(request.POST.get(
                                'phone'), request.POST.get('email'), pass1)
                            my_user.save()
                            send_mail(
                                'Account Verification',
                                'please waiting for account verification.your account status will updated in mail',
                                'bookingbus770@gmail.com',
                                [em],
                                fail_silently=False,
                            )
                            return redirect('login')
                    else:
                        messages.error(request, "Some Problem in data..")
                        return render(request, "registration.html")

                except Exception as e:
                    v = str(e)
                    print(v)
                    messages.error(request, v)
                    return render(request, 'registration.html')
        else:
            messages.error(request, 'Travel Agency is save successfully..!')
    else:
        return render(request, 'registration.html')


def handle_uploaded_file(f):
    file_path = path.join(os.getcwd(), "media", "file", f.name)
    print(file_path)
    file = open(file_path, 'w+')
    print(f.chunks())
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def check(request):
    return render(request, "check.html")


def edit(request, id):
    saveschedule = schedule.objects.get(id=id)
    schedule_date = saveschedule.date
    schedule_time = saveschedule.time
    print(schedule_time)
    sh = schedule_time.hour
    smin = schedule_time.minute
    sm = schedule_date.month
    sy = schedule_date.year
    sd = schedule_date.day
    if sm < 10:
        sm = "0" + str(sm)
    if sd < 10:
        sd = "0" + str(sd)
    if sh < 10:
        sh = "0" + str(sh)
    if smin < 10:
        smin = "0" + str(smin)

    schedule_time = saveschedule.time
    print(schedule_date)
    if request.method == "POST":

        if request.POST.get('form') and request.POST.get('optradio') and request.POST.get('to') and request.POST.get(
                'date') and request.POST.get('time') and request.POST.get('date') and request.POST.get(
                'total_seat') and request.POST.get('date') and request.POST.get('window') and request.POST.get(
                'date') and request.POST.get('general') and request.POST.get('date') and request.POST.get(
                'price') and request.POST.get('date') and request.POST.get('bus_number'):
            saveschedule = schedule()
            travel = Verified_travel_agency.objects.get(
                id=request.session['um'])
            print(request.POST.get('optradio'))
            saveschedule.form = request.POST.get('form')
            saveschedule.date = request.POST.get('date')
            saveschedule.time = request.POST.get('time')
            saveschedule.to = request.POST.get('to')
            saveschedule.bus_number = request.POST.get('bus_number')
            saveschedule.bus_type = request.POST.get('optradio')
            saveschedule.price = request.POST.get('price')
            saveschedule.total_seats = request.POST.get('total_seat')
            saveschedule.window = request.POST.get('window')
            saveschedule.general = request.POST.get('general')
            saveschedule.agency_number = request.session['um']
            saveschedule.agency_name = travel.agency_name
            saveschedule.pk = request.session['um'] + \
                              request.POST.get('bus_number')
            messages.success(request, "schedule successfully added")
            total = int(request.POST.get('total_seat'))
            window = int(request.POST.get('window'))
            general = int(request.POST.get('general'))
            if total == window + general:
                try:
                    saveschedule.save()
                    messages.success(request, "schedule successfully updated")
                    return redirect('history')
                except:
                    messages.error(request, "please enter valid data")
            else:
                messages.error(request, "please enter valid data")

    return render(request, 'edit.html',
                  {'data': saveschedule, 'dd': schedule_date, 'm': sm, 'y': sy, 'd': sd, 'tm': schedule_time, 'h': sh,
                   'min': smin})


def profile(request):
    id = request.session['um']
    showdata = Verified_travel_agency.objects.get(id=id)

    return render(request, 'profile.html', {'data': showdata})


def adentry(request):
    if request.method == "POST":

        if request.POST.get('phone') and request.POST.get('email') and request.POST.get('password'):

            saverecord = admin()
            saverecord.pk = request.POST.get('phone')
            saverecord.mobile_no = request.POST.get('phone')
            saverecord.password = request.POST.get('password')
            saverecord.email = request.POST.get('email')
            # print(saverecord.file)
            saverecord.save()
            my_user = User.objects.create_user(request.POST.get(
                'phone'), request.POST.get('email'), request.POST.get('password'))
            my_user.save()

            messages.success(request, 'admin ' +
                             saverecord.mobile_no + ' is save successfully..!')
            return redirect('login')
        else:

            messages.success(request, 'admin is save successfully..!')

    else:
        return render(request, 'entry.html')


def showemp(request):
    showem = travel_agency.objects.all()
    showvm = Verified_travel_agency.objects.all()
    return render(request, 'fetch_travel_agecy_details.html', {'data': showem, 'data2': showvm})


def approve(request, id):
    savedata = Verified_travel_agency()
    edit2 = travel_agency.objects.get(id=id)
    savedata.agency_name = edit2.agency_name
    savedata.address = edit2.address
    savedata.aadhar_no = edit2.aadhar_no
    savedata.email = edit2.email
    savedata.pk = edit2.pk
    savedata.password = edit2.password
    savedata.mobile_no = edit2.mobile_no
    savedata.file = edit2.file
    savedata.save()
    edit2.status = "True"
    edit2.save()
    print(edit2.status)
    messages.success(request, "travel agency successfully approved ")
    if messages.success:
        send_mail(
            'Account Verification',
            savedata.agency_name +
            ' is successfully verified by admin,now you can able to login to System',
            'bookingbus770@gmail.com',
            [savedata.email],
            fail_silently=False,
        )
    return redirect('adhome')


def aprroved(request):
    showem = Verified_travel_agency.objects.all()
    return render(request, 'aproved_list.html', {'data': showem})


def dell(request, id):
    edit2 = travel_agency.objects.get(id=id)
    em = edit2.email
    User.objects.get(username=id).delete()
    edit2.delete()
    messages.success(request, "travel agency successfully removed ")
    if messages.success:
        send_mail(
            'Account Confirmation',
            'your account is not verified by admin,please enter the valid information while registration,thank you',
            'bookingbus770@gmail.com',
            [em],
            fail_silently=False,
        )
    return redirect('adhome')
    # return render(request,"fetch_travel_agency_details.html",{"data1":edit2,'data':showem})


def signup_user(request):
    if request.method == "POST":
        pass1 = request.POST.get('password')
        pass2 = request.POST.get('password1')
        if request.POST.get('uname') and request.POST.get('phone') and request.POST.get('email') and request.POST.get(
                'password') and request.POST.get('password1'):
            if pass1 != pass2:
                messages.error(
                    request, "your password and confirm password are not same")
                return render(request, "signup_user.html",
                              {"uname": request.POST.get('uname'), "email": request.POST.get('email'),
                               "phone": request.POST.get('phone')})
            else:
                try:
                    saverecord = user()
                    saverecord.user_name = request.POST.get('uname')
                    saverecord.pk = request.POST.get('phone')
                    saverecord.mobile_no = request.POST.get('phone')
                    saverecord.password = request.POST.get('password')
                    saverecord.email = request.POST.get('email')
                    my_user = User.objects.create_user(request.POST.get(
                        'phone'), request.POST.get('email'), pass1)
                    my_user.save()
                    saverecord.save()
                    messages.success(
                        request, saverecord.user_name + ' is save successfully..!')
                    if messages.success:
                        send_mail(
                            'Account Registration',
                            saverecord.user_name + ',Thank you for register to the System',
                            '22ceuod003@ddu.ac.in',
                            [saverecord.email],
                            fail_silently=False,
                        )
                        return redirect('login')
                except:
                    messages.error(request, "User Already exist...")
                    return render(request, 'signup_user.html')

    else:
        return render(request, 'signup_user.html')


def usersu(request):
    return render(request, 'home.html')


def user_home(request):
    if request.method == "POST":
        showschedule = schedule.objects.all()
        for s in showschedule:
            if s.date == request.POST.get('date'):
                sr = s.date
                break
        s = request.POST.get('date')
        datetime_str = s
        datetime_object = datetime.strptime(datetime_str, '%Y-%m-%d').date()
        m = datetime_object.strftime("%B")
        dm = datetime_object.day
        d = datetime_object.day
        y = datetime_object.year

        dt = datetime_object.strftime(m + ' %d, %Y')
        print(dt)
        if request.POST.get('form') and request.POST.get('to') and request.POST.get('date'):
            form = request.POST.get('form')
            to = request.POST.get('to')
            date = request.POST.get('date')
            showschedule = schedule.objects.all()
            quers = schedule.objects.filter(date=date, form=form, to=to)
            return render(request, 'searched_list.html',
                          {'date': date, 'form': form, 'to': to, 'schedule': showschedule, 'dt': dt, 'dc': quers})

    else:
        return render(request, 'userhome.html')


def booking(request, id):
    request.session['amount'] = ""
    booking = schedule.objects.get(id=id)
    customer = user.objects.get(id=request.session['um'])
    adds = request.POST.get("addseat")
    if request.method == "POST":
        if request.POST.get('addseat') and request.POST.get('sc'):
            seat = request.POST.get("sc")
            adds = request.POST.get("addseat")
            if seat == "window":
                if int(adds) <= int(booking.window):
                    orderamount = int(adds) * int(booking.price) * 100
                    amount = int(adds) * int(booking.price)
                    client = razorpay.Client(
                        auth=("rzp_test_ULKXFl3prtGM7z", "IQyDNCHgqTTcZj1SGroTb0Cl"))
                    payment = client.order.create({'amount': orderamount, 'currency': 'INR',
                                                   'payment_capture': '1'})
                    print(orderamount)
                    request.session['amount'] = orderamount
                    return render(request, "index.html",
                                  {'amount1': amount, 'amount': orderamount, 'bustype': booking.bus_type,
                                   'from': booking.form, 'to': booking.to, 'date': booking.date, 'time': booking.time,
                                   'aname': booking.agency_name, 'tseat': booking.total_seats, 'window': booking.window,
                                   'General': booking.general, 'price': booking.price, 'cname': customer.user_name,
                                   'id': booking.id, 'adds': adds, 'type': 'Window', "busnumber": booking.bus_number,
                                   "bustype": booking.bus_type, "anumber": booking.agency_number})
                else:
                    messages.error(request, "not Available Seats...")
                    return render(request, "booking.html",
                                  {'bustype': booking.bus_type, 'from': booking.form, 'to': booking.to,
                                   'date': booking.date, 'time': booking.time, 'aname': booking.agency_name,
                                   'tseat': booking.total_seats, 'window': booking.window, 'General': booking.general,
                                   'price': booking.price, 'cname': customer.user_name})
            else:
                if int(adds) <= int(booking.general):
                    orderamount = int(adds) * int(booking.price) * 100
                    amount = int(adds) * int(booking.price)

                    client = razorpay.Client(
                        auth=("rzp_test_ULKXFl3prtGM7z", "IQyDNCHgqTTcZj1SGroTb0Cl"))

                    payment = client.order.create({'amount': orderamount, 'currency': 'INR',
                                                   'payment_capture': '1'})
                    print(orderamount)
                    request.session['amount'] = orderamount
                    return render(request, "index.html",
                                  {'amount1': amount, 'amount': orderamount, 'bustype': booking.bus_type,
                                   'from': booking.form, 'to': booking.to, 'date': booking.date, 'time': booking.time,
                                   'aname': booking.agency_name, 'tseat': booking.total_seats, 'window': booking.window,
                                   'General': booking.general, 'price': booking.price, 'cname': customer.user_name,
                                   'id': booking.id, 'adds': adds, 'type': 'General', "busnumber": booking.bus_number,
                                   "bustype": booking.bus_type, "anumber": booking.agency_number})
                else:
                    messages.error(request, "not Available Seats...")
                    return render(request, "booking.html",
                                  {'bustype': booking.bus_type, 'from': booking.form, 'to': booking.to,
                                   'date': booking.date, 'time': booking.time, 'aname': booking.agency_name,
                                   'tseat': booking.total_seats, 'window': booking.window, 'General': booking.general,
                                   'price': booking.price, 'cname': customer.user_name})

    return render(request, "booking.html",
                  {'bustype': booking.bus_type, 'from': booking.form, 'to': booking.to, 'date': booking.date,
                   'time': booking.time, 'aname': booking.agency_name, 'tseat': booking.total_seats,
                   'window': booking.window, 'General': booking.general, 'price': booking.price,
                   'cname': customer.user_name})


def success(request):
    print(request.POST.get('mp'))
    print(request.POST.get("payment"))
    abc = request.POST.get("totalseat")
    print(abc)

    num = random.randint(10000, 99999)
    booking = ticket()
    if request.method == "POST":
        if request.POST.get('type') == "General":
            generalseat = request.POST.get("totalseat")
            totalseat = schedule.objects.get(id=request.POST.get('mp'))
            availableseat = int(totalseat.total_seats) - int(generalseat)
            availablegenralseat = int(totalseat.general) - int(generalseat)
            totalseat.total_seats = availableseat
            totalseat.general = availablegenralseat
            totalseat.save()
            booking.ticketid = num
            booking.pk = num
            booking.b_from = request.POST.get('from')
            booking.b_to = request.POST.get('to')
            booking.seat_type = request.POST.get('type')
            booking.bus_type = request.POST.get('bustype')
            booking.time = request.POST.get('time')
            booking.date = request.POST.get('date')
            booking.booking_time = datetime.now()
            booking.Customer_name = request.POST.get('cname')
            booking.Customer_number = request.session['um']
            booking.Agency_name = request.POST.get('agency_name')
            booking.Agency_number = request.POST.get('anumber')
            booking.Seats = abc
            booking.amount = request.POST.get("total")
            booking.bus_number = request.POST.get("busnumber")

            booking.save()
            customer = user.objects.get(id=request.session['um'])
            email = str(customer.email)
            try:
                send_mail(
                    'Ticket Booking',
                    request.POST.get('cname') + ',Thank you for Book ticket \nTicket id:' + str(
                        num) + '\n From: ' + request.POST.get('from') + '\t to:' + request.POST.get(
                        'to') + '\n Bus Number:' + request.POST.get('busnumber') + '\t bus type:' +
                    request.POST.get('bustype') + '\t Seats:' + abc + '\t Seat type:' + request.POST.get(
                        'type') + '\nDate:' + request.POST.get(
                        'date') + '\n Time:' + request.POST.get('time') + '\n Amount:' + request.POST.get(
                        'total') + '\u20B9',
                    'bookingbus770@gmail.com',
                    [email],
                    fail_silently=False,
                )
            except SMTPException as e:
                messages.error(
                    "There was an error sending an email but don't worry, your ticket if successfully Confirmed ")
                return render(request, "success.html",
                              {"anumber": request.POST.get('anumber'), "amount": request.POST.get("total"),
                               "tseat": abc, "id": request.POST.get('totalseat'), "type": request.POST.get('type'),
                               "date": request.POST.get('date'), "time": request.POST.get('time'),
                               "cname": request.POST.get('cname'), "aname": request.POST.get("agency_name"),
                               "from": request.POST.get("from"), "to": request.POST.get("to"),
                               "busnumber": request.POST.get("busnumber"), "bustype": request.POST.get("bustype")})

        if request.POST.get('type') == "Window":
            generalseat = request.POST.get("totalseat")
            totalseat = schedule.objects.get(id=request.POST.get('mp'))
            availableseat = int(totalseat.total_seats) - int(generalseat)
            availablegenralseat = int(totalseat.window) - int(generalseat)
            totalseat.total_seats = availableseat
            totalseat.window = availablegenralseat
            totalseat.save()
            booking.ticketid = num
            booking.pk = num
            booking.b_from = request.POST.get('from')
            booking.b_to = request.POST.get('to')
            booking.seat_type = request.POST.get('type')
            booking.bus_type = request.POST.get('bustype')
            booking.time = request.POST.get('time')
            booking.date = request.POST.get('date')
            booking.booking_time = datetime.now()
            booking.Customer_name = request.POST.get('cname')
            booking.Customer_number = request.session['um']
            booking.Agency_name = request.POST.get('agency_name')
            booking.Agency_number = request.POST.get('anumber')
            booking.Seats = abc
            booking.amount = request.POST.get("total")
            booking.bus_number = request.POST.get("busnumber")
            booking.save()
            customer = user.objects.get(id=request.session['um'])
            email = str(customer.email)
            try:
                send_mail(
                    'Ticket Booking',
                    request.POST.get('cname') + ',Thank you for Book ticket \nTicket id:' + str(
                        num) + '\n From: ' + request.POST.get('from') + '\t to:' + request.POST.get(
                        'to') + '\n Bus Number:' + request.POST.get('busnumber') + '\t bus type:' +
                    request.POST.get('bustype') + '\t Seats:' + abc + '\n Seat type:' + request.POST.get(
                        'type') + '\nDate:' + request.POST.get(
                        'date') + '\n Time:' + request.POST.get('time') + '\n Amount:' + request.POST.get(
                        'total') + '\u20B9',
                    'bookingbus770@gmail.com',
                    [email],
                    fail_silently=False,
                )
            except SMTPException as e:
                messages.error(
                    "There was an error sending an email but don't :your ticket if successfully Confirmed ")
                return render(request, "success.html",
                              {"anumber": request.POST.get('anumber'), "amount": request.POST.get("total"),
                               "tseat": abc, "id": request.POST.get('totalseat'), "type": request.POST.get('type'),
                               "date": request.POST.get('date'), "time": request.POST.get('time'),
                               "cname": request.POST.get('cname'), "aname": request.POST.get("agency_name"),
                               "from": request.POST.get("from"), "to": request.POST.get("to"),
                               "busnumber": request.POST.get("busnumber"), "bustype": request.POST.get("bustype")})

    return render(request, "success.html",
                  {"anumber": request.POST.get('anumber'), "amount": request.POST.get("total"), "tseat": abc,
                   "id": request.POST.get('totalseat'), "type": request.POST.get('type'),
                   "date": request.POST.get('date'), "time": request.POST.get('time'),
                   "cname": request.POST.get('cname'), "aname": request.POST.get("agency_name"),
                   "from": request.POST.get("from"), "to": request.POST.get("to"),
                   "busnumber": request.POST.get("busnumber"), "bustype": request.POST.get("bustype")})


def ticket_list(request):
    abc = ticket.objects.filter(Customer_number=request.session['um'])
    return render(request, "booking_list.html", {"ticket_list": abc})


def download(request, id):
    bus = ticket.objects.get(id=id)
    b_from = bus.b_from
    agency = Verified_travel_agency.objects.get(id=bus.Agency_number)
    return render(request, "download.html",
                  {"from": b_from, "to": bus.b_to, "btime": bus.booking_time, "cname": bus.Customer_name,
                   "cnumber": bus.Customer_number, "aname": bus.Agency_name, "address": agency.address,
                   "anumber": bus.Agency_number, "busnumber": bus.bus_number, "seattype": bus.seat_type,
                   "btype": bus.bus_type, "tid": bus.id, "seats": bus.Seats, "amount": bus.amount, "date": bus.date,
                   "time": bus.time})


def uprofile(request):
    abc = user.objects.get(id=request.session['um'])
    return render(request, "user_profile.html", {"Name": abc.user_name, "mobile": abc.mobile_no, "email": abc.email})


def booklist(request):
    data = schedule.objects.filter(agency_number=request.session['um'])
    return render(request, "book_ticket_list.html", {'data': data})


def customers_list(request, id):
    t = ticket.objects.filter(bus_number=id)
    return render(request, "customer_list.html", {"data": t, "num": id})


def list_download(request, id):
    t = ticket.objects.filter(bus_number=id)
    return render(request, "download_list.html", {"data": t, "bnumber": id})
# Create your views here.
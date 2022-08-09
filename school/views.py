from io import BytesIO
from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from django.core.mail import send_mail

"""
import từ code tự làm
"""
# import file
import datetime as dt
import pandas as pd
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User

# tìm kiếm
from django.db.models import Q
from django.contrib import messages


# Code tự làm
khoi_id_selected = "5"                   # id của khối được chọn
lop_selected = ""                       # id của lớp được chọn

khoi_status = "Toàn trường"               # Tên Khối được chọn
lop_status = "Chọn lớp"                 # Tên Lớp được chọn

list_khoi = models.Khoi.objects.all()          # Các object của Khối
list_lop =[]                            # Các object của Lớp
list_hs=[]                                 # Các object của HS


def search_hs(request):
    
    global khoi_id_selected
      
    global list_khoi
    global list_hs
    global khoi_id_selected
    global khoi_status
    global lop_status
    # ten_lop_selected = ""
    
    # print('khoi_id_selected', khoi_id_selected)
    # print('lop_selected', lop_selected)
    print('lop_status', lop_status)
    if request.method == 'GET':
        form_tk = forms.FormTim_kiem(request.GET)                
        if form_tk.is_valid():            
            chuoi_tim_kiem = form_tk.cleaned_data['chuoi_tim_kiem'] 
            list_lop = models.Lop.objects.filter(ma_khoi_id=khoi_id_selected)
            # print(list_lop)
            if chuoi_tim_kiem!='':
                if khoi_id_selected != '5':
                    if lop_selected =="":
                        print('Toàn khối')
                        print("Khối chọn ", khoi_id_selected)                        
                        print("Lớp chọn ", lop_selected)       
                        print(list_lop)    
                                      
                        list_id_lop=[]
                        for id_lop in list(list_lop.values()):
                            # print(id_lop['id'])
                            list_id_lop.append(id_lop['id'])
                        print(list(list_id_lop))
                        list_hs = models.StudentExtra.objects.filter(
                            Q(ma_lop_id__in=list_id_lop),
                            Q(ho_ten__contains= chuoi_tim_kiem) |Q(ngay_sinh__contains=chuoi_tim_kiem)
                            |Q(ma_hs__contains=chuoi_tim_kiem)
                        ).order_by("ho_ten")
                        
                    else:
                        print('Chọn lớp')
                        print("Khối chọn ", khoi_id_selected)                        
                        print("Lớp chọn ", lop_selected) 
                        print("lop_status",lop_status)
                        lop_status = list_lop.get(id=lop_selected).ten_lop
                        list_hs = models.StudentExtra.objects.filter(
                            Q(ma_lop_id = str(lop_selected)),
                            Q(ho_ten__contains= chuoi_tim_kiem)
                            |Q(ngay_sinh__contains=chuoi_tim_kiem)
                            |Q(ma_hs__contains=chuoi_tim_kiem)                                                                                                                
                        ).order_by("ho_ten")
                        # print(list_hs)
                else:
                    print("toàn trường")
                    print("Khối chọn ", khoi_id_selected)                        
                    print("Lớp chọn ", lop_selected) 
                    # print('chuoi_tim_kiem',chuoi_tim_kiem)
                    list_hs = models.StudentExtra.objects.filter(                                                                                         
                        Q(ho_ten__contains= chuoi_tim_kiem)
                        |Q(ngay_sinh__contains=chuoi_tim_kiem)
                        |Q(ma_hs__contains=chuoi_tim_kiem) 
                    ).order_by("ho_ten")
                    # print('chuoi_tim_kiem',chuoi_tim_kiem)
                    print('list_hs',list_hs)
                    
    khoi_status = models.Khoi.objects.get(pk=khoi_id_selected).ten_khoi
    # print('khoi_status',khoi_status)  
    # print('lop_status',lop_status)      
                               
    return render(request,'school/admin_view_student.html',{                       
                  'students':list_hs,
                  'list_khoi':list_khoi,
                  'list_lop':list_lop,
                  'khoi_status':khoi_status,
                  'lop_status':lop_status,
                  'form_tk':form_tk,
              })

def import_diem(request) :
    try:
        if request.method=="POST" and request.FILES['myfile2']:
            myfile = request.FILES['myfile2']
            print("myfile2",myfile)
            print("myfile2.name",myfile.name)
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            print("filename",filename)
            uploaded_file_url = fs.url(filename)
            excel_file = uploaded_file_url
            print("excel_file",excel_file)
            # empexceldata = pd.read_excel("." + excel_file, encoding='utf-8')        
            empexceldata = pd.read_excel("." + excel_file) 
            print(empexceldata)
            df = empexceldata
            
            # Dùng df.loc[label] để truy xuất dòng
            for i in range(len(df)):   
                #Update Điểm 
                hoc_sinh = models.StudentExtra.objects.get(id=df.loc[i,"id"])
                
                hoc_sinh.diem_toan = df.loc[i,'diem_toan']
                hoc_sinh.gv_toan_id = df.loc[i,'gv_toan_id']
                hoc_sinh.mon_toan_id = df.loc[i,'mon_toan_id']
                
                hoc_sinh.diem_ly = df.loc[i,'diem_ly']
                hoc_sinh.gv_ly_id = df.loc[i,'gv_ly_id']
                hoc_sinh.mon_ly_id = df.loc[i,'mon_ly_id']
                
                hoc_sinh.diem_hoa = df.loc[i,'diem_hoa']
                hoc_sinh.gv_hoa_id = df.loc[i,'gv_hoa_id']
                hoc_sinh.mon_hoa_id = df.loc[i,'mon_hoa_id']
                
                hoc_sinh.diem_van = df.loc[i,'diem_van']
                hoc_sinh.gv_van_id = df.loc[i,'gv_van_id']
                hoc_sinh.mon_van_id = df.loc[i,'mon_van_id']
                
                hoc_sinh.diem_ngoai_ngu = df.loc[i,'diem_ngoai_ngu']
                hoc_sinh.gv_ngoai_ngu_id = df.loc[i,'gv_ngoai_ngu_id']
                hoc_sinh.mon_ngoai_ngu_id = df.loc[i,'mon_ngoai_ngu_id']
                
                hoc_sinh.diem_tb = round(df.loc[i,'diem_tb'],1)
                hoc_sinh.save()
    except Exception as identifier:
        print(identifier)
    return render(request, 'school/admin_import_diem.html')


def khoi_filter(request,khoi_id):
    
    global khoi_id_selected
    global lop_selected
    global list_hs
    # global khoi_status
    # global lop_status
    # global list_hs
    # global list_lop
    
    # Lưu khoi_id vào khoi_id_selected
    khoi_id_selected = khoi_id
    lop_selected = ""
    list_lop = models.Lop.objects.filter(ma_khoi_id=khoi_id_selected)       
    khoi_status = models.Khoi.objects.get(pk=khoi_id_selected).ten_khoi
    lop_status = "Chọn lớp"    
    
    # Nếu một khối được chọn thì list_hs sẽ là hs của các lớp thuộc khối được chọn
    if khoi_id < 5:
        list_id_lop=[]
        for id_lop in list(list_lop.values()):
            # print(id_lop['id'])
            list_id_lop.append(id_lop['id'])
        # print(list_id_lop)
        list_hs = models.StudentExtra.objects.filter(ma_lop_id__in=list_id_lop)
    
    # Nếu khối = 5 thì là toàn trường
    if khoi_id==5:
        # ten_khoi = "các Khối"
        list_hs = models.StudentExtra.objects.all()
        
        
    form_tk = forms.FormTim_kiem(request.GET)       
    # print(list_khoi)
    
    print('khoi_id_selected', khoi_id_selected)
    print('lop_selected', lop_selected)
    return render(request, 'school/admin_view_student.html', {        
        'students':list_hs,
        'list_khoi':list_khoi,
        'list_lop':list_lop,
        'khoi_id_selected':khoi_id_selected,
        'khoi_status':khoi_status,
        'lop_status':lop_status,
        'form_tk':form_tk
        })

def gv_khoi_filter(request,khoi_id):
    global khoi_id_selected
    global lop_selected
    global list_hs
    # global khoi_status
    # global lop_status
    # global list_hs
    # global list_lop
    
    # Lưu khoi_id vào khoi_id_selected
    khoi_id_selected = khoi_id
    lop_selected = ""
    list_lop = models.Lop.objects.filter(ma_khoi_id=khoi_id_selected)       
    khoi_status = models.Khoi.objects.get(pk=khoi_id_selected).ten_khoi
    lop_status = "Chọn lớp"    
    
    # Nếu một khối được chọn thì list_hs sẽ là hs của các lớp thuộc khối được chọn
    if khoi_id < 5:
        list_id_lop=[]
        for id_lop in list(list_lop.values()):
            # print(id_lop['id'])
            list_id_lop.append(id_lop['id'])
        # print(list_id_lop)
        list_hs = models.StudentExtra.objects.filter(ma_lop_id__in=list_id_lop)
    
    # Nếu khối = 5 thì là toàn trường
    if khoi_id==5:
        # ten_khoi = "các Khối"
        list_hs = models.StudentExtra.objects.all()
        
    form_tk = forms.FormTim_kiem(request.GET)       

    return render(request, 'school/gv_view_hs.html', {        
        'students':list_hs,
        'list_khoi':list_khoi,
        'list_lop':list_lop,
        'khoi_id_selected':khoi_id_selected,
        'khoi_status':khoi_status,
        'lop_status':lop_status,
        'form_tk':form_tk
        })
    
def hs_khoi_filter(request,khoi_id):
    global khoi_id_selected
    global lop_selected
    global list_hs
    # global khoi_status
    # global lop_status
    # global list_hs
    # global list_lop
    
    # Lưu khoi_id vào khoi_id_selected
    khoi_id_selected = khoi_id
    lop_selected = ""
    list_lop = models.Lop.objects.filter(ma_khoi_id=khoi_id_selected)       
    khoi_status = models.Khoi.objects.get(pk=khoi_id_selected).ten_khoi
    lop_status = "Chọn lớp"    
    
    # Nếu một khối được chọn thì list_hs sẽ là hs của các lớp thuộc khối được chọn
    if khoi_id < 5:
        list_id_lop=[]
        for id_lop in list(list_lop.values()):
            # print(id_lop['id'])
            list_id_lop.append(id_lop['id'])
        # print(list_id_lop)
        list_hs = models.StudentExtra.objects.filter(ma_lop_id__in=list_id_lop)
    
    # Nếu khối = 5 thì là toàn trường
    if khoi_id==5:
        # ten_khoi = "các Khối"
        list_hs = models.StudentExtra.objects.all()
        
    form_tk = forms.FormTim_kiem(request.GET)       
    # print(list_khoi)
    return render(request, 'school/hs_view_hs.html', {        
        'students':list_hs,
        'list_khoi':list_khoi,
        'list_lop':list_lop,
        'khoi_id_selected':khoi_id_selected,
        'khoi_status':khoi_status,
        'lop_status':lop_status,
        'form_tk':form_tk
        })
    
    
def gv_lop_filter(request, lop_id):
    global khoi_id_selected
    global lop_selected
    global list_hs
    # global list_lop
    # global list_hs
    # global lop_status
    
       
    lop_selected = lop_id
    list_lop = models.Lop.objects.filter(id=lop_selected)
    lop_status = list_lop.get(id=lop_selected).ten_lop
    khoi_id_selected = list_lop.get(id=lop_selected).ma_khoi_id
    khoi_status = models.Khoi.objects.get(id=khoi_id_selected).ten_khoi
    list_lop = models.Lop.objects.filter(ma_khoi_id=khoi_id_selected)
    print(list_lop)
    list_hs = models.StudentExtra.objects.filter(ma_lop=lop_id)         
    form_tk = forms.FormTim_kiem(request.GET)    
    
    
    print('khoi_status',khoi_status)  
    print('lop_status',lop_status)        
    return render(request, 'school/gv_view_hs.html', {            
        'students':list_hs,
        'list_khoi':list_khoi,
        'list_lop':list_lop,
        'khoi_id_selected':khoi_id_selected,
        'khoi_status':khoi_status,
        'lop_selected':lop_selected,
        'lop_status':lop_status,
        'form_tk':form_tk})

def hs_lop_filter(request, lop_id):
    global khoi_id_selected
    global lop_selected
    global list_hs
    # global list_lop
    # global list_hs
    # global lop_status
    
       
    lop_selected = lop_id
    list_lop = models.Lop.objects.filter(id=lop_selected)
    lop_status = list_lop.get(id=lop_selected).ten_lop
    khoi_id_selected = list_lop.get(id=lop_selected).ma_khoi_id
    khoi_status = models.Khoi.objects.get(id=khoi_id_selected).ten_khoi
    list_lop = models.Lop.objects.filter(ma_khoi_id=khoi_id_selected)
    print(list_lop)
    list_hs = models.StudentExtra.objects.filter(ma_lop=lop_id)         
    form_tk = forms.FormTim_kiem(request.GET)    
    
    
    print('khoi_status',khoi_status)  
    print('lop_status',lop_status)        
    return render(request, 'school/hs_view_hs.html', {            
        'students':list_hs,
        'list_khoi':list_khoi,
        'list_lop':list_lop,
        'khoi_id_selected':khoi_id_selected,
        'khoi_status':khoi_status,
        'lop_selected':lop_selected,
        'lop_status':lop_status,
        'form_tk':form_tk})

def lop_filter(request,lop_id):   
    global khoi_id_selected
    global lop_selected
    global list_hs
    # global list_lop
    # global list_hs
    # global lop_status
    
       
    lop_selected = lop_id
    list_lop = models.Lop.objects.filter(id=lop_selected)
    lop_status = list_lop.get(id=lop_selected).ten_lop
    khoi_id_selected = list_lop.get(id=lop_selected).ma_khoi_id
    khoi_status = models.Khoi.objects.get(id=khoi_id_selected).ten_khoi
    list_lop = models.Lop.objects.filter(ma_khoi_id=khoi_id_selected)
    print(list_lop)
    list_hs = models.StudentExtra.objects.filter(ma_lop=lop_id)         
    form_tk = forms.FormTim_kiem(request.GET)    
    
    
    print('khoi_status',khoi_status)  
    print('lop_status',lop_status)        
    return render(request, 'school/admin_view_student.html', {            
        'students':list_hs,
        'list_khoi':list_khoi,
        'list_lop':list_lop,
        'khoi_id_selected':khoi_id_selected,
        'khoi_status':khoi_status,
        'lop_selected':lop_selected,
        'lop_status':lop_status,
        'form_tk':form_tk})
    
# Tạo mã học sinh
def create_code(id_num,user_type="HS"):
    # id_text có 5 chữ số xxxx
    id_text = str(id_num)   
    for i in range(5-len(id_text)):
        id_text = '0' + id_text    
    return user_type + id_text

# Hàm thêm học sinh 
def them_user(user_name):
    # Add User
    username = password = user_name
    print("username",username)
    user = User.objects.create(username=username,first_name=username)
    u = User.objects.get(username__exact=username)
    u.set_password(password)
    u.save()
    # Add Group
    my_student_group = Group.objects.get_or_create(name='STUDENT')
    my_student_group[0].user_set.add(user)
    print('my_student_group[0]',my_student_group[0])
        
    return 

def export_hs(request):
    global list_hs
    # students=models.StudentExtra.objects.all()
    students = list_hs
    
    df = pd.DataFrame(list(students.values()))
    print(df)
    # Ghi ra file excel vào folder của project
    # df.to_excel('pandas_to_excel.xlsx', sheet_name='new_sheet_name')
    
    # Xuất file ra browser
    with BytesIO() as b:
        # Use the StringIO object as the filehandle.
        writer = pd.ExcelWriter(b, engine='openpyxl')
        df.to_excel(writer, sheet_name='Sheet1')
        writer.save()
        # Set up the Http response.
        filename = 'danh_sach.xlsx'
        response = HttpResponse(
            b.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        return response

# Nhập danh sách học sinh vào    
def import_hs(request):
    # Nếu table Hoc_sinh chưa có dữ liệu thì thực hiện Query sẽ báo lỗi
    # Do đó dùng try để bắt lỗi
    try:
        id_set = models.StudentExtra.objects.latest('id')
        last_id = id_set.id
    except models.StudentExtra.DoesNotExist:
        last_id = 0
    # print("last_id",last_id)
                       
    try:
        if request.method=="POST" and request.FILES['myfile']:
            # Đọc file vào dataframe
            myfile = request.FILES['myfile']
            # print("myfile",myfile)
            # print("myfile.name",myfile.name)
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            # print("filename",filename)
            uploaded_file_url = fs.url(filename)
            excel_file = uploaded_file_url
            # print("excel_file",excel_file)
            # empexceldata = pd.read_excel("." + excel_file, encoding='utf-8')        
            empexceldata = pd.read_excel("." + excel_file) 
            df = empexceldata
            print(df)
            
            # Ghi vào tabe StudentExtra
            # Dùng df.loc[label] để truy xuất dòng
            for i in range(len(df)):    
                last_id = last_id + 1             
                ma_hs = create_code(last_id,"HS")  
                # print(ma_hs)    
                
                them_user(ma_hs)   
                print("ma_hs",ma_hs)    
                                 
                ma_lop_id = df.loc[i, "ma_lop_id"] 
                gvcn_id = df.loc[i, "gvcn_id"]             
                ho_ten = df.loc[i, "ho_ten"]
                # dt là datetime đã import
                ngay_sinh = df.loc[i, "ngay_sinh"] #dt.datetime.strptime(df.loc[i, "ngay_sinh"]) , ("%d/%m/%Y", "%Y-%m-%d"))
                gioi_tinh = df.loc[i, "gioi_tinh"]    
                dia_chi = df.loc[i, "dia_chi"]
                phu_huynh = df.loc[i, "phu_huynh"]
                phone_phu_huynh = df.loc[i, "phone_phu_huynh"]
                ghi_chu = df.loc[i, "ghi_chu"]
                
                # Thêm tạm giá trị cho Student            
                roll = "STUDENT"
                mobile = "0123456"
                fee = 123
                cl= 'one'

                # Ghi và table Hoc_sinh
                
                hoc_sinh = models.StudentExtra.objects.create(
                    user_id = User.objects.get(username=ma_hs).id,
                    ma_hs = ma_hs,                         
                    ma_lop_id = ma_lop_id,  
                    gvcn_id = gvcn_id,              
                    ho_ten = ho_ten,                    
                    ngay_sinh = ngay_sinh,
                    gioi_tinh = gioi_tinh,
                    dia_chi = dia_chi,
                    phu_huynh = phu_huynh,
                    phone_phu_huynh = phone_phu_huynh,
                    ghi_chu = ghi_chu,
                    
                    # Thêm tạm giá trị cho Student 
                    roll = "STUDENT",
                    mobile = "0123456",
                    fee = 123,
                    cl= 'one',
                    status=True,
                )                
                hoc_sinh.save()
            
            
    except Exception as identifier:
        print(identifier)
        
    # return render(request, 'school/importexcel.html',{})
    return render(request, 'school/admin_import_hs.html',{})

def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'school/index.html')



#for showing signup/login button for teacher
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'school/adminclick.html')


#for showing signup/login button for teacher
def teacherclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'school/teacherclick.html')


#for showing signup/login button for student
def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'school/studentclick.html')





def admin_signup_view(request):
    form=forms.AdminSigupForm()
    if request.method=='POST':
        form=forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()


            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)

            return HttpResponseRedirect('adminlogin')
    return render(request,'school/adminsignup.html',{'form':form})




def student_signup_view(request):
    form1=forms.StudentUserForm()
    form2=forms.StudentExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.StudentUserForm(request.POST)
        form2=forms.StudentExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            user2=f2.save()

            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)

        return HttpResponseRedirect('studentlogin')
    return render(request,'school/studentsignup.html',context=mydict)


def teacher_signup_view(request):
    form1=forms.TeacherUserForm()
    form2=forms.TeacherExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.TeacherUserForm(request.POST)
        form2=forms.TeacherExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            user2=f2.save()

            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)

        return HttpResponseRedirect('teacherlogin')
    return render(request,'school/teachersignup.html',context=mydict)



#for checking user is techer , student or admin
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()
def is_student(user):
    return user.groups.filter(name='STUDENT').exists()


def afterlogin_view(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_teacher(request.user):
        accountapproval=models.TeacherExtra.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('teacher-dashboard')
        else:
            return render(request,'school/teacher_wait_for_approval.html')
    elif is_student(request.user):
        accountapproval=models.StudentExtra.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('student-dashboard')
        else:
            return render(request,'school/student_wait_for_approval.html')




#for dashboard of adminnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    teachercount=models.TeacherExtra.objects.all().filter(status=True).count()
    pendingteachercount=models.TeacherExtra.objects.all().filter(status=False).count()

    studentcount=models.StudentExtra.objects.all().filter(status=True).count()
    pendingstudentcount=models.StudentExtra.objects.all().filter(status=False).count()

    teachersalary=models.TeacherExtra.objects.filter(status=True).aggregate(Sum('salary'))
    pendingteachersalary=models.TeacherExtra.objects.filter(status=False).aggregate(Sum('salary'))

    studentfee=models.StudentExtra.objects.filter(status=True).aggregate(Sum('fee',default=0))
    pendingstudentfee=models.StudentExtra.objects.filter(status=False).aggregate(Sum('fee'))

    notice=models.Notice.objects.all()

    #aggregate function return dictionary so fetch data from dictionay
    mydict={
        'teachercount':teachercount,
        'pendingteachercount':pendingteachercount,

        'studentcount':studentcount,
        'pendingstudentcount':pendingstudentcount,

        'teachersalary':teachersalary['salary__sum'],
        'pendingteachersalary':pendingteachersalary['salary__sum'],

        'studentfee':studentfee['fee__sum'],
        'pendingstudentfee':pendingstudentfee['fee__sum'],

        'notice':notice

    }

    return render(request,'school/admin_dashboard.html',context=mydict)







#for teacher sectionnnnnnnn by adminnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_teacher_view(request):
    return render(request,'school/admin_teacher.html')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_teacher_view(request):
    form1=forms.TeacherUserForm()
    form2=forms.TeacherExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.TeacherUserForm(request.POST)
        form2=forms.TeacherExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()

            f2=form2.save(commit=False)
            f2.user=user
            f2.status=True
            f2.save()

            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-teacher')
    return render(request,'school/admin_add_teacher.html',context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_teacher_view(request):
    teachers=models.TeacherExtra.objects.all().filter(status=True)
    return render(request,'school/admin_view_teacher.html',{'teachers':teachers})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_teacher_view(request):
    teachers=models.TeacherExtra.objects.all().filter(status=False)
    return render(request,'school/admin_approve_teacher.html',{'teachers':teachers})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_teacher_view(request,pk):
    teacher=models.TeacherExtra.objects.get(id=pk)
    teacher.status=True
    teacher.save()
    return redirect(reverse('admin-approve-teacher'))


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_teacher_view(request,pk):
    teacher=models.TeacherExtra.objects.get(id=pk)
    user=models.User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return redirect('admin-approve-teacher')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_teacher_from_school_view(request,pk):
    teacher=models.TeacherExtra.objects.get(id=pk)
    user=models.User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return redirect('admin-view-teacher')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_teacher_view(request,pk):
    teacher=models.TeacherExtra.objects.get(id=pk)
    user=models.User.objects.get(id=teacher.user_id)

    form1=forms.TeacherUserForm(instance=user)
    form2=forms.TeacherExtraForm(instance=teacher)
    mydict={'form1':form1,'form2':form2}

    if request.method=='POST':
        form1=forms.TeacherUserForm(request.POST,instance=user)
        form2=forms.TeacherExtraForm(request.POST,instance=teacher)
        print(form1)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.status=True
            f2.save()
            return redirect('admin-view-teacher')
    return render(request,'school/admin_update_teacher.html',context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_teacher_salary_view(request):
    teachers=models.TeacherExtra.objects.all()
    return render(request,'school/admin_view_teacher_salary.html',{'teachers':teachers})






#for student by adminnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_student_view(request):
    return render(request,'school/admin_student.html')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_student_view(request):
    form1=forms.StudentUserForm()
    form2=forms.StudentExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.StudentUserForm(request.POST)
        form2=forms.StudentExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            print("form is valid")
            user=form1.save()
            user.set_password(user.password)
            user.save()

            f2=form2.save(commit=False)
            f2.user=user
            f2.status=True
            f2.save()

            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
        else:
            print("form is invalid")
        return HttpResponseRedirect('admin-student')
    return render(request,'school/admin_add_student.html',context=mydict)

def teacher_hs_view(request):
    # global list_khoi
    
    
    students=models.StudentExtra.objects.all().filter(status=True)
    khoi_status = "Toàn trường"
    list_khoi = models.Khoi.objects.all()
    print("list_khoi",list_khoi)
    
    form_tk = forms.FormTim_kiem(request.GET) 
    return render(request,'school/gv_view_hs.html',{        
        'students':students,
        # 'list_tim_kiem':list_tim_kiem,
        'list_hs':list_hs,
        'list_khoi':list_khoi,
        'khoi_status':khoi_status,
        'lop_status':lop_status,
        'form_tk':form_tk,
        
        })
    
def hs_hs_view(request):
    # global list_khoi
    
    
    students=models.StudentExtra.objects.all().filter(status=True)
    khoi_status = "Toàn trường"
    list_khoi = models.Khoi.objects.all()
    print("list_khoi",list_khoi)
    
    form_tk = forms.FormTim_kiem(request.GET) 
    return render(request,'school/hs_view_hs.html',{        
        'students':students,
        # 'list_tim_kiem':list_tim_kiem,
        'list_hs':list_hs,
        'list_khoi':list_khoi,
        'khoi_status':khoi_status,
        'lop_status':lop_status,
        'form_tk':form_tk,
        
        })    

def teacher_search_hs(request):
    global khoi_id_selected
      
    global list_khoi
    global list_hs
    global khoi_id_selected
    global khoi_status
    global lop_status
    # ten_lop_selected = ""
    
    # print('khoi_id_selected', khoi_id_selected)
    # print('lop_selected', lop_selected)
    print('lop_status', lop_status)
    if request.method == 'GET':
        form_tk = forms.FormTim_kiem(request.GET)                
        if form_tk.is_valid():            
            chuoi_tim_kiem = form_tk.cleaned_data['chuoi_tim_kiem'] 
            list_lop = models.Lop.objects.filter(ma_khoi_id=khoi_id_selected)
            # print(list_lop)
            if chuoi_tim_kiem!='':
                if khoi_id_selected != '5':
                    if lop_selected =="":
                        print('Toàn khối')
                        print("Khối chọn ", khoi_id_selected)                        
                        print("Lớp chọn ", lop_selected)       
                        print(list_lop)    
                                      
                        list_id_lop=[]
                        for id_lop in list(list_lop.values()):
                            # print(id_lop['id'])
                            list_id_lop.append(id_lop['id'])
                        print(list(list_id_lop))
                        list_hs = models.StudentExtra.objects.filter(
                            Q(ma_lop_id__in=list_id_lop),
                            Q(ho_ten__contains= chuoi_tim_kiem) |Q(ngay_sinh__contains=chuoi_tim_kiem)
                            |Q(ma_hs__contains=chuoi_tim_kiem)
                        ).order_by("ho_ten")
                        
                    else:
                        print('Chọn lớp')
                        print("Khối chọn ", khoi_id_selected)                        
                        print("Lớp chọn ", lop_selected) 
                        print("lop_status",lop_status)
                        lop_status = list_lop.get(id=lop_selected).ten_lop
                        list_hs = models.StudentExtra.objects.filter(
                            Q(ma_lop_id = str(lop_selected)),
                            Q(ho_ten__contains= chuoi_tim_kiem)
                            |Q(ngay_sinh__contains=chuoi_tim_kiem)
                            |Q(ma_hs__contains=chuoi_tim_kiem)                                                                                                                
                        ).order_by("ho_ten")
                        # print(list_hs)
                else:
                    print("toàn trường")
                    print("Khối chọn ", khoi_id_selected)                        
                    print("Lớp chọn ", lop_selected) 
                    # print('chuoi_tim_kiem',chuoi_tim_kiem)
                    list_hs = models.StudentExtra.objects.filter(                                                                                         
                        Q(ho_ten__contains= chuoi_tim_kiem)
                        |Q(ngay_sinh__contains=chuoi_tim_kiem)
                        |Q(ma_hs__contains=chuoi_tim_kiem) 
                    ).order_by("ho_ten")
                    # print('chuoi_tim_kiem',chuoi_tim_kiem)
                    print('list_hs',list_hs)
                    
    khoi_status = models.Khoi.objects.get(pk=khoi_id_selected).ten_khoi
    # print('khoi_status',khoi_status)  
    # print('lop_status',lop_status)      
                               
    return render(request,'school/hs_view_hs.html',{                       
                  'students':list_hs,
                  'list_khoi':list_khoi,
                  'list_lop':list_lop,
                  'khoi_status':khoi_status,
                  'lop_status':lop_status,
                  'form_tk':form_tk,
              })
    
    
def hs_search_hs(request):
    global khoi_id_selected
      
    global list_khoi
    global list_hs
    global khoi_id_selected
    global khoi_status
    global lop_status
    # ten_lop_selected = ""
    
    # print('khoi_id_selected', khoi_id_selected)
    # print('lop_selected', lop_selected)
    print('lop_status', lop_status)
    if request.method == 'GET':
        form_tk = forms.FormTim_kiem(request.GET)                
        if form_tk.is_valid():            
            chuoi_tim_kiem = form_tk.cleaned_data['chuoi_tim_kiem'] 
            list_lop = models.Lop.objects.filter(ma_khoi_id=khoi_id_selected)
            # print(list_lop)
            if chuoi_tim_kiem!='':
                if khoi_id_selected != '5':
                    if lop_selected =="":
                        print('Toàn khối')
                        print("Khối chọn ", khoi_id_selected)                        
                        print("Lớp chọn ", lop_selected)       
                        print(list_lop)    
                                      
                        list_id_lop=[]
                        for id_lop in list(list_lop.values()):
                            # print(id_lop['id'])
                            list_id_lop.append(id_lop['id'])
                        print(list(list_id_lop))
                        list_hs = models.StudentExtra.objects.filter(
                            Q(ma_lop_id__in=list_id_lop),
                            Q(ho_ten__contains= chuoi_tim_kiem) |Q(ngay_sinh__contains=chuoi_tim_kiem)
                            |Q(ma_hs__contains=chuoi_tim_kiem)
                        ).order_by("ho_ten")
                        
                    else:
                        print('Chọn lớp')
                        print("Khối chọn ", khoi_id_selected)                        
                        print("Lớp chọn ", lop_selected) 
                        print("lop_status",lop_status)
                        lop_status = list_lop.get(id=lop_selected).ten_lop
                        list_hs = models.StudentExtra.objects.filter(
                            Q(ma_lop_id = str(lop_selected)),
                            Q(ho_ten__contains= chuoi_tim_kiem)
                            |Q(ngay_sinh__contains=chuoi_tim_kiem)
                            |Q(ma_hs__contains=chuoi_tim_kiem)                                                                                                                
                        ).order_by("ho_ten")
                        # print(list_hs)
                else:
                    print("toàn trường")
                    print("Khối chọn ", khoi_id_selected)                        
                    print("Lớp chọn ", lop_selected) 
                    # print('chuoi_tim_kiem',chuoi_tim_kiem)
                    list_hs = models.StudentExtra.objects.filter(                                                                                         
                        Q(ho_ten__contains= chuoi_tim_kiem)
                        |Q(ngay_sinh__contains=chuoi_tim_kiem)
                        |Q(ma_hs__contains=chuoi_tim_kiem) 
                    ).order_by("ho_ten")
                    # print('chuoi_tim_kiem',chuoi_tim_kiem)
                    print('list_hs',list_hs)
                    
    khoi_status = models.Khoi.objects.get(pk=khoi_id_selected).ten_khoi
    # print('khoi_status',khoi_status)  
    # print('lop_status',lop_status)      
                               
    return render(request,'school/hs_view_hs.html',{                       
                  'students':list_hs,
                  'list_khoi':list_khoi,
                  'list_lop':list_lop,
                  'khoi_status':khoi_status,
                  'lop_status':lop_status,
                  'form_tk':form_tk,
              })   
    
    

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_student_view(request):
    # global list_khoi
    
    
    students=models.StudentExtra.objects.all().filter(status=True)
    khoi_status = "Toàn trường"
    list_khoi = models.Khoi.objects.all()
    print("list_khoi",list_khoi)
    
    form_tk = forms.FormTim_kiem(request.GET) 
    return render(request,'school/admin_view_student.html',{        
        'students':students,
        # 'list_tim_kiem':list_tim_kiem,
        'list_hs':list_hs,
        'list_khoi':list_khoi,
        'khoi_status':khoi_status,
        'lop_status':lop_status,
        'form_tk':form_tk,
        
        })


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_student_from_school_view(request,pk):
    student=models.StudentExtra.objects.get(id=pk)
    user=models.User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return redirect('admin-view-student')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_student_view(request,pk):
    student=models.StudentExtra.objects.get(id=pk)
    user=models.User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return redirect('admin-approve-student')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_student_view(request,pk):
    student=models.StudentExtra.objects.get(id=pk)
    user=models.User.objects.get(id=student.user_id)
    form1=forms.StudentUserForm(instance=user)
    form2=forms.StudentExtraForm(instance=student)
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.StudentUserForm(request.POST,instance=user)
        form2=forms.StudentExtraForm(request.POST,instance=student)
        print(form1)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.status=True
            f2.save()
            return redirect('admin-view-student')
    return render(request,'school/admin_update_student.html',context=mydict)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_student_view(request):
    students=models.StudentExtra.objects.all().filter(status=False)
    return render(request,'school/admin_approve_student.html',{'students':students})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_student_view(request,pk):
    students=models.StudentExtra.objects.get(id=pk)
    students.status=True
    students.save()
    return redirect(reverse('admin-approve-student'))


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_student_fee_view(request):
    students=models.StudentExtra.objects.all()
    return render(request,'school/admin_view_student_fee.html',{'students':students})






#attendance related viewwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_attendance_view(request):
    return render(request,'school/admin_attendance.html')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_take_attendance_view(request,cl):
    students=models.StudentExtra.objects.all().filter(cl=cl)
    print(students)
    aform=forms.AttendanceForm()
    if request.method=='POST':
        form=forms.AttendanceForm(request.POST)
        if form.is_valid():
            Attendances=request.POST.getlist('present_status')
            date=form.cleaned_data['date']
            for i in range(len(Attendances)):
                AttendanceModel=models.Attendance()
                AttendanceModel.cl=cl
                AttendanceModel.date=date
                AttendanceModel.present_status=Attendances[i]
                AttendanceModel.roll=students[i].roll
                AttendanceModel.save()
            return redirect('admin-attendance')
        else:
            print('form invalid')
    return render(request,'school/admin_take_attendance.html',{'students':students,'aform':aform})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_attendance_view(request,cl):
    form=forms.AskDateForm()
    if request.method=='POST':
        form=forms.AskDateForm(request.POST)
        if form.is_valid():
            date=form.cleaned_data['date']
            attendancedata=models.Attendance.objects.all().filter(date=date,cl=cl)
            studentdata=models.StudentExtra.objects.all().filter(cl=cl)
            mylist=zip(attendancedata,studentdata)
            return render(request,'school/admin_view_attendance_page.html',{'cl':cl,'mylist':mylist,'date':date})
        else:
            print('form invalid')
    return render(request,'school/admin_view_attendance_ask_date.html',{'cl':cl,'form':form})









#fee related view by adminnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_fee_view(request):
    return render(request,'school/admin_fee.html')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_fee_view(request,cl):
    feedetails=models.StudentExtra.objects.all().filter(cl=cl)
    return render(request,'school/admin_view_fee.html',{'feedetails':feedetails,'cl':cl})








#notice related viewsssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_notice_view(request):
    form=forms.NoticeForm()
    if request.method=='POST':
        form=forms.NoticeForm(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            form.by=request.user.first_name
            form.save()
            return redirect('admin-dashboard')
    return render(request,'school/admin_notice.html',{'form':form})








#for TEACHER  LOGIN    SECTIONNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_dashboard_view(request):
    teacherdata=models.TeacherExtra.objects.all().filter(status=True,user_id=request.user.id)
    notice=models.Notice.objects.all()
    mydict={
        'salary':teacherdata[0].salary,
        'mobile':teacherdata[0].mobile,
        'date':teacherdata[0].joindate,
        'notice':notice
    }
    return render(request,'school/teacher_dashboard.html',context=mydict)



@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_attendance_view(request):
    return render(request,'school/teacher_attendance.html')


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_take_attendance_view(request,cl):
    students=models.StudentExtra.objects.all().filter(cl=cl)
    aform=forms.AttendanceForm()
    if request.method=='POST':
        form=forms.AttendanceForm(request.POST)
        if form.is_valid():
            Attendances=request.POST.getlist('present_status')
            date=form.cleaned_data['date']
            for i in range(len(Attendances)):
                AttendanceModel=models.Attendance()
                AttendanceModel.cl=cl
                AttendanceModel.date=date
                AttendanceModel.present_status=Attendances[i]
                AttendanceModel.roll=students[i].roll
                AttendanceModel.save()
            return redirect('teacher-attendance')
        else:
            print('form invalid')
    return render(request,'school/teacher_take_attendance.html',{'students':students,'aform':aform})



@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_attendance_view(request,cl):
    form=forms.AskDateForm()
    if request.method=='POST':
        form=forms.AskDateForm(request.POST)
        if form.is_valid():
            date=form.cleaned_data['date']
            attendancedata=models.Attendance.objects.all().filter(date=date,cl=cl)
            studentdata=models.StudentExtra.objects.all().filter(cl=cl)
            mylist=zip(attendancedata,studentdata)
            return render(request,'school/teacher_view_attendance_page.html',{'cl':cl,'mylist':mylist,'date':date})
        else:
            print('form invalid')
    return render(request,'school/teacher_view_attendance_ask_date.html',{'cl':cl,'form':form})



@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_notice_view(request):
    form=forms.NoticeForm()
    if request.method=='POST':
        form=forms.NoticeForm(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            form.by=request.user.first_name
            form.save()
            return redirect('teacher-dashboard')
        else:
            print('form invalid')
    return render(request,'school/teacher_notice.html',{'form':form})







#FOR STUDENT AFTER THEIR Loginnnnnnnnnnnnnnnnnnnnn
@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_dashboard_view(request):
    studentdata=models.StudentExtra.objects.all().filter(status=True,user_id=request.user.id)
    notice=models.Notice.objects.all()
    mydict={
        'roll':studentdata[0].roll,
        'mobile':studentdata[0].mobile,
        'fee':studentdata[0].fee,
        'notice':notice
    }
    return render(request,'school/student_dashboard.html',context=mydict)



@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_attendance_view(request):
    form=forms.AskDateForm()
    if request.method=='POST':
        form=forms.AskDateForm(request.POST)
        if form.is_valid():
            date=form.cleaned_data['date']
            studentdata=models.StudentExtra.objects.all().filter(user_id=request.user.id,status=True)
            attendancedata=models.Attendance.objects.all().filter(date=date,cl=studentdata[0].cl,roll=studentdata[0].roll)
            mylist=zip(attendancedata,studentdata)
            return render(request,'school/student_view_attendance_page.html',{'mylist':mylist,'date':date})
        else:
            print('form invalid')
    return render(request,'school/student_view_attendance_ask_date.html',{'form':form})









# for aboutus and contact ussssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss
def aboutus_view(request):
    return render(request,'school/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'school/contactussuccess.html')
    return render(request, 'school/contactus.html', {'form':sub})

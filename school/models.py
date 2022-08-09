from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Nien_khoa(models.Model):
    nien_khoa = models.CharField(max_length=9, null=False)
    nien_khoa_tit = models.CharField(max_length=200,blank=True, null=True)

    def __str__(self):
        return self.nien_khoa
    
class Khoi(models.Model):
    ma_khoi = models.SmallIntegerField()
    ten_khoi = models.CharField(max_length=100,blank=True, null=True)
    khoi_tit = models.CharField(max_length=200,blank=True, null=True)

    def __str__(self):
        return self.ten_khoi
# class Giao_vien(models.Model):
#     ma_gv = models.CharField(max_length=10,blank=True, null=True)
#     ten_gv = models.CharField(max_length=30)
#     gioi_tinh = models.CharField(max_length=10)
#     phone = models.CharField(max_length=10,blank=True, null=True)
#     email = models.EmailField(blank=True, null=True)

# class Lop(models.Model):
#     ma_lop = models.CharField(max_length=10)
#     ten_lop = models.CharField(max_length=50)
#     nien_khoa = models.ForeignKey(Nien_khoa, on_delete=models.PROTECT)
#     ma_gv = models.ForeignKey(Giao_vien, on_delete=models.PROTECT)
#     ma_khoi = models.ForeignKey(Khoi, on_delete=models.PROTECT)

#     def __str__(self):
#         return self.ten_lop
    
class Mon_hoc(models.Model):
    ma_mon = models.CharField(max_length=10, null=True)
    ten_mon = models.CharField(max_length=50, null=True)
    ma_khoi = models.ForeignKey(Khoi, on_delete=models.PROTECT)
    mon_tit = models.CharField(max_length=200,blank=True, null=True)

    def __str__(self):
        return self.ten_mon

class TeacherExtra(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    salary = models.PositiveIntegerField(null=False)
    joindate=models.DateField(auto_now_add=True)
    mobile = models.CharField(max_length=40)
    status=models.BooleanField(default=False)
    ### Dữ liệu từ Giao_vien
    ma_gv = models.CharField(max_length=10,blank=True, null=True)
    ten_gv = models.CharField(max_length=30, null=True)
    gioi_tinh = models.CharField(max_length=10, null=True)
    phone = models.CharField(max_length=10,blank=True, null=True)

    def __str__(self):
        return self.user.first_name
    @property
    def get_id(self):
        return self.user.id
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name

class Lop(models.Model):
    ma_lop = models.CharField(max_length=10)
    ten_lop = models.CharField(max_length=50)
    nien_khoa = models.ForeignKey(Nien_khoa, on_delete=models.PROTECT)
    ma_gv = models.ForeignKey(TeacherExtra, on_delete=models.PROTECT)
    ma_khoi = models.ForeignKey(Khoi, on_delete=models.PROTECT)

    def __str__(self):
        return self.ten_lop

gioitinh=[('Nam','Nam'),('Nữ','Nữ')]
classes=[('one','one'),('two','two'),('three','three'),
('four','four'),('five','five'),('six','six'),('seven','seven'),('eight','eight'),('nine','nine'),('ten','ten')]
class StudentExtra(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    roll = models.CharField(max_length=10, null=True)
    mobile = models.CharField(max_length=40,null=True)
    fee=models.PositiveIntegerField(null=True)
    cl= models.CharField(max_length=10,choices=classes,default='one')
    status=models.BooleanField(default=False)
    ### Dữ Liệu từ Hoc_sinh
    ma_hs = models.CharField(max_length=10, null=True)
    ma_lop = models.ForeignKey(Lop, on_delete=models.PROTECT,blank=True, null=True)   
    gvcn = models.ForeignKey(TeacherExtra, on_delete=models.PROTECT,blank=True, null=True, related_name='+') 
    ho_ten = models.CharField(max_length=100,blank=True, null=True)
    ngay_sinh = models.DateField(blank=True, null=True)   
    gioi_tinh = models.CharField(max_length=10,choices=gioitinh,blank=True, null=True) 
    dia_chi = models.CharField(max_length=150,blank=True, null=True)
    phu_huynh = models.CharField(max_length=150,blank=True, null=True)
    phone_phu_huynh = models.CharField(max_length=10,blank=True, null=True)
    
    # Toán
    gv_toan = models.ForeignKey(TeacherExtra,on_delete=models.PROTECT,blank=True, null=True, related_name='+')    
    mon_toan = models.ForeignKey(Mon_hoc,on_delete=models.PROTECT,blank=True, null=True, related_name='+')
    diem_toan = models.FloatField(blank=True, null=True)
    # Văn
    gv_van = models.ForeignKey(TeacherExtra,on_delete=models.PROTECT,blank=True, null=True, related_name='+')    
    mon_van = models.ForeignKey(Mon_hoc,on_delete=models.PROTECT,blank=True, null=True, related_name='+')
    diem_van = models.FloatField(blank=True, null=True)
    # Ngoại ngữ
    gv_ngoai_ngu = models.ForeignKey(TeacherExtra,on_delete=models.PROTECT,blank=True, null=True, related_name='+')    
    mon_ngoai_ngu = models.ForeignKey(Mon_hoc,on_delete=models.PROTECT,blank=True, null=True, related_name='+')
    diem_ngoai_ngu = models.FloatField(blank=True, null=True)
    # Lý
    gv_ly = models.ForeignKey(TeacherExtra,on_delete=models.PROTECT,blank=True, null=True, related_name='+')    
    mon_ly = models.ForeignKey(Mon_hoc,on_delete=models.PROTECT,blank=True, null=True, related_name='+')
    diem_ly = models.FloatField(blank=True, null=True)
    # Hóa
    gv_hoa = models.ForeignKey(TeacherExtra,on_delete=models.PROTECT,blank=True, null=True, related_name='+')    
    mon_hoa = models.ForeignKey(Mon_hoc,on_delete=models.PROTECT,blank=True, null=True, related_name='+')
    diem_hoa = models.FloatField(blank=True, null=True)        
    
    diem_tb = models.FloatField(blank=True, null=True)
    ghi_chu = models.TextField(max_length=350, blank=True, null=True)
    
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name



class Attendance(models.Model):
    roll=models.CharField(max_length=10,null=True)
    date=models.DateField()
    cl=models.CharField(max_length=10)
    present_status = models.CharField(max_length=10)



class Notice(models.Model):
    date=models.DateField(auto_now=True)
    by=models.CharField(max_length=20,null=True,default='school')
    message=models.CharField(max_length=500)
    
class Tim_kiem(models.Model):
    tim_kiem_id = models.SmallIntegerField()
    ten_tim_kiem = models.CharField(max_length=100,blank=True, null=True)
    ghi_chu = models.CharField(max_length=255,blank=True, null=True)
    chuoi_tim_kiem = models.CharField(max_length=255,blank=True, null=True)

    def __str__(self):
        return self.ten_tim_kiem
# Generated by Django 3.0.5 on 2022-07-15 13:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0012_giao_vien_hoc_sinh_khoi_lop_mon_hoc_nien_khoa'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hoc_sinh',
            name='gv_hoa',
        ),
        migrations.RemoveField(
            model_name='hoc_sinh',
            name='gv_ly',
        ),
        migrations.RemoveField(
            model_name='hoc_sinh',
            name='gv_ngoai_ngu',
        ),
        migrations.RemoveField(
            model_name='hoc_sinh',
            name='gv_toan',
        ),
        migrations.RemoveField(
            model_name='hoc_sinh',
            name='gv_van',
        ),
        migrations.RemoveField(
            model_name='hoc_sinh',
            name='gvcn',
        ),
        migrations.RemoveField(
            model_name='hoc_sinh',
            name='ma_lop',
        ),
        migrations.RemoveField(
            model_name='hoc_sinh',
            name='mon_hoa',
        ),
        migrations.RemoveField(
            model_name='hoc_sinh',
            name='mon_ly',
        ),
        migrations.RemoveField(
            model_name='hoc_sinh',
            name='mon_ngoai_ngu',
        ),
        migrations.RemoveField(
            model_name='hoc_sinh',
            name='mon_toan',
        ),
        migrations.RemoveField(
            model_name='hoc_sinh',
            name='mon_van',
        ),
        migrations.AddField(
            model_name='studentextra',
            name='dia_chi',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='studentextra',
            name='diem_hoa',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='studentextra',
            name='diem_ly',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='studentextra',
            name='diem_ngoai_ngu',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='studentextra',
            name='diem_tb',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='studentextra',
            name='diem_toan',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='studentextra',
            name='diem_van',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='studentextra',
            name='ghi_chu',
            field=models.TextField(blank=True, max_length=350, null=True),
        ),
        migrations.AddField(
            model_name='studentextra',
            name='gioi_tinh',
            field=models.CharField(blank=True, choices=[('Nam', 'Nam'), ('N???', 'N???')], max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='studentextra',
            name='gv_hoa',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='school.TeacherExtra'),
        ),
        migrations.AddField(
            model_name='studentextra',
            name='gv_ly',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='school.TeacherExtra'),
        ),
        migrations.AddField(
            model_name='studentextra',
            name='gv_ngoai_ngu',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='school.TeacherExtra'),
        ),
        migrations.AddField(
            model_name='studentextra',
            name='gv_toan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='school.TeacherExtra'),
        ),
        migrations.AddField(
            model_name='studentextra',
            name='gv_van',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='school.TeacherExtra'),
        ),
        migrations.AddField(
            model_name='studentextra',
            name='gvcn',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='school.TeacherExtra'),
        ),
        migrations.AddField(
            model_name='studentextra',
            name='ho_ten',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='studentextra',
            name='ma_hs',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='studentextra',
            name='ma_lop',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='school.Lop'),
        ),
        migrations.AddField(
            model_name='studentextra',
            name='mon_hoa',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='school.Mon_hoc'),
        ),
        migrations.AddField(
            model_name='studentextra',
            name='mon_ly',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='school.Mon_hoc'),
        ),
        migrations.AddField(
            model_name='studentextra',
            name='mon_ngoai_ngu',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='school.Mon_hoc'),
        ),
        migrations.AddField(
            model_name='studentextra',
            name='mon_toan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='school.Mon_hoc'),
        ),
        migrations.AddField(
            model_name='studentextra',
            name='mon_van',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='school.Mon_hoc'),
        ),
        migrations.AddField(
            model_name='studentextra',
            name='ngay_sinh',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='studentextra',
            name='phone_phu_huynh',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='studentextra',
            name='phu_huynh',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='teacherextra',
            name='gioi_tinh',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='teacherextra',
            name='ma_gv',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='teacherextra',
            name='phone',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='teacherextra',
            name='ten_gv',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='lop',
            name='ma_gv',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='school.TeacherExtra'),
        ),
        migrations.DeleteModel(
            name='Giao_vien',
        ),
        migrations.DeleteModel(
            name='Hoc_sinh',
        ),
    ]

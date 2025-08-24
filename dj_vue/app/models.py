from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.

class Rel(models.Model):
    obj_name = models.CharField('结点1名称',max_length=20,default='')
    obj_type = models.CharField('结点1类型', max_length=20, default='')
    rel_name = models.CharField('关系名称', max_length=20, default='')
    rel_type = models.CharField('关系类型', max_length=20, default='')
    sub_name = models.CharField('结点2名称', max_length=20, default='')
    sub_type = models.CharField('结点2类型', max_length=20, default='')

    def __str__(self):
        return '<%s>->[%s]-><%s>'%(self.obj_name,self.rel_name,self.sub_name);

    class Meta:
        db_table='Rel'
        verbose_name='关系表'
        verbose_name_plural=verbose_name

SEX=(
    ('男','男'),
    ('女','女'),
)


class alldata(models.Model):
    uuid = models.UUIDField(primary_key=True, verbose_name="uuid", auto_created=True, default=uuid.uuid4,
                            editable=False)
    k1=models.TextField('地点',default='')
    k2=models.TextField('建立时间',default='')
    k3=models.TextField('建立朝代',default='')
    k4=models.TextField('地址',default='')
    k5=models.TextField('面积',default='')
    k6=models.TextField('简介',default='')
    class Meta:
        db_table='alldata'
        verbose_name='数据表'
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.userName





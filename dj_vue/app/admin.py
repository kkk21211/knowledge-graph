from django.contrib import admin

# Register your models here.
from .models import Rel, alldata

admin.site.site_header = '遗迹知识图谱系统'  # 设置header
admin.site.site_title = '遗迹知识图谱系统'   # 设置title
admin.site.index_title = '遗迹知识图谱系统'

@admin.register(Rel)
class RelAdmin(admin.ModelAdmin):
    list_display = ("obj_name","obj_type","rel_name","rel_type","sub_name","sub_type")# 要显示哪些信息
    # list_display_links = ('id','name')#点击哪些信息可以进入编辑页面
    search_fields = ["obj_name","obj_type","rel_name","rel_type","sub_name","sub_type"]   #指定要搜索的字段，将会出现一个搜索框让管理员搜索关键词
    list_filter =["obj_name","obj_type","rel_name","rel_type","sub_name","sub_type"]#指定列表过滤器，右边将会出现一个快捷的过滤选项
@admin.register(alldata)
class alldataAdmin(admin.ModelAdmin):
    list_display = ('k1','k2','k3','k4','k5','k6')  # 要显示哪些信息
    search_fields = ['k1','k2','k3','k4','k5','k6']  # 指定要搜索的字段，将会出现一个搜索框让管理员搜索关键词
    list_filter = ['k1','k2','k3','k4','k5','k6']  # 指定列表过滤器，右边将会出现一个快捷的过滤选项




from django.contrib import admin
from BookingApp.models import Speech, Student, BookingOrder

# Register your models here.

admin.site.site_header = "贵大讲座信息平台管理"

@admin.register(Speech)
class SpeechAdmin(admin.ModelAdmin):
    list_display = [
        'speech_add_time',
        'speech_name',
        'speech_speaker_name',
        'speech_time',
        'speech_place',
        'speech_capacity',
        'speech_chair_remain_number',
    ]
    search_fields = [
        'speech_add_time',
        'speech_name',
        'speech_speaker_name',
        'speech_time',
        'speech_place',
        'speech_capacity',
        'speech_chair_remain_number',
    ]

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = [
        'stu_number',
        'stu_name',
        'stu_college',
        'stu_class',
        'stu_phone_number',
    ]
    search_fields = [
        'stu_number',
        'stu_name',
        'stu_college',
        'stu_class',
        'stu_phone_number',
    ]

@admin.register(BookingOrder)
class BookingOrderAdmin(admin.ModelAdmin):
    list_display = [
        'order_time',
        'speech_name',
        'order_stu_name',
    ]
    search_fields = [
        'order_time',
        'speech_name',
        'order_stu_name',
    ]

    def speech_name(self, obj):
        objs = Speech.objects.filter(id__exact=obj.order_speech_id)
        return "".join([x.speech_name for x in objs])

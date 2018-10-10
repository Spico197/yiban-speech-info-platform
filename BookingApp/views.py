from django.shortcuts import render
from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from .models import Speech, Student, BookingOrder
import requests
import json

get_code_url = "https://openapi.yiban.cn/oauth/authorize?client_id={}&redirect_uri={}".format("<client_id>", "<redirect_uri>")
# get_access_token_url = "https://openapi.yiban.cn/oauth/access_token?client_id=7d852327ca8c9ced&client_secret=be4bd736cc4fd609172e72b300bdb52d&code={}&redirect_uri=http://39.108.7.66:2333/".format(code)

class YibanId(object):
    def __init__(self, *args, **kwargs):
        self.code = ""
        self.access_token = ""
        self.yiban_id = ""

def me(access_token):
    url = "https://openapi.yiban.cn/user/me?access_token=" + access_token
    re = requests.get(url)
    # print("me interface before json return")
    return json.loads(re.text)

def detail(request):
    query = request.GET.get("id")
    detail_obj = Speech.objects.get(id=int(query))
    # print(detail_obj.speech_capacity, BookingOrder.objects.filter(order_speech_id__exact=int(query)).count())
    detail_obj.speech_chair_remain_number = detail_obj.speech_capacity - BookingOrder.objects.filter(order_speech_id__exact=int(query)).count()
    detail_obj.save()
    context = {
        "item": detail_obj,
    }
    return render(request, "detail.html", context=context)

def get_oauth(request):
    return HttpResponseRedirect(get_code_url)

def booking_yiban(request):
    ok = ""
    if request.GET:
        stu_id = request.session.get("yiban_id")
        stu_name = request.session.get("username")
        speech_id = request.GET.get("id")
        speech_id = int(speech_id)

        speech_obj = Speech.objects.get(id=speech_id)
        detail_obj = Speech.objects.get(id=speech_id)
        # print(stu_id, stu_name, speech_id)
        try:
            if stu_id and stu_name and speech_id:
                if speech_obj.speech_chair_remain_number > 0:
                    # print("booking process 1")
                    if BookingOrder.objects.filter(order_stu_number__exact=stu_id, order_speech_id=speech_id).count() == 0:
                        # print("booking process 2")
                        obj = BookingOrder.objects.create(
                            order_speech_id=speech_id,
                            order_stu_number=stu_id,
                            order_stu_phone_number="",
                            order_stu_name=stu_name
                        )
                        obj.save()
                        speech_obj.speech_chair_remain_number = speech_obj.speech_capacity - BookingOrder.objects.filter(order_speech_id__exact=speech_id).count()
                        speech_obj.save()
                        if obj.id:
                            ok = "预定成功！"
                        else:
                            ok = "预定失败！"
                    else:
                        ok = "您已经预定过！"
                else:
                    ok = "预定失败，座位已满！"
            else:
                ok = "预定失败，请确认您已正常登录！"
        except Exception:
            ok = "预定失败！"
        context = {
            "item": detail_obj,
            "ok": ok
        }
    else:
        ok = "请使用GET方法访问，并使用易班授权登录预定~"
        query = request.GET.get("id")
        detail_obj = Speech.objects.get(id=int(query))
        context = {
            "item": detail_obj,
            "ok": ok,
        }
    return render(request, "booking-yiban.html", context=context)

def booking(request):
    ok = ""
    if request.POST:
        stu_id = request.POST.get("stu_id")
        stu_name = request.POST.get("stu_name")
        stu_phone = request.POST.get("stu_phone")
        speech_id = request.POST.get("id")
        speech_id = int(speech_id)

        speech_obj = Speech.objects.get(id=speech_id)
        detail_obj = Speech.objects.get(id=speech_id)
        # try:
        if Student.objects.filter(stu_number__exact=stu_id, stu_name__exact=stu_name).count() > 0 and speech_obj.speech_chair_remain_number > 0:
            # print("booking process 1")
            if BookingOrder.objects.filter(order_stu_number__exact=stu_id, order_speech_id=speech_id).count() == 0:
                # print("booking process 2")
                obj = BookingOrder.objects.create(
                    order_speech_id=speech_id,
                    order_stu_number=stu_id,
                    order_stu_phone_number=stu_phone,
                    order_stu_name=stu_name
                )
                obj.save()
                speech_obj.speech_chair_remain_number = speech_obj.speech_capacity - BookingOrder.objects.filter(order_speech_id__exact=speech_id).count()
                speech_obj.save()
                if obj.id:
                    ok = "预定成功！"
                else:
                    ok = "预定失败！"
            else:
                ok = "您已经预定过！"
        else:
            ok = "预定失败！"
        # except Exception:
        #     ok = "预定失败！"
        context = {
            "item": detail_obj,
            "ok": ok
        }
    else:
        query = request.GET.get("id")
        detail_obj = Speech.objects.get(id=int(query))
        context = {
            "item": detail_obj,
        }
    return render(request, "booking.html", context=context)

def booking_list(request):
    stu_id = request.session.get("yiban_id")
    items = BookingOrder.objects.filter(order_stu_number__exact=stu_id).order_by("-order_time")
    print("items = ", list(items))
    speech_ids = [x.order_speech_id for x in items]
    print("speech_ids = ", speech_ids)
    item = []
    for speech_id in speech_ids:
        item.append(Speech.objects.get(id=speech_id))
    print("item = ", item)
    user = request.session.get("username") + "，点击注销"
    link = "/logout/"

    limit = 10
    paginator = Paginator(item, limit)
    page = request.GET.get('page', 1)
    loaded = paginator.page(page)

    context = {
        "all_title": "用户预定清单",
        'ArticleInfo': loaded,
        "user": user,
        "link": link
    }
    return render(request, "booking-list.html", context=context)

def cancel_booking(request):
    if request.GET.get("id"):
        speech_cancel_id = request.GET.get("id")
        booking_obj = BookingOrder.objects.get(order_speech_id=speech_cancel_id, order_stu_number=request.session.get("yiban_id"))
        booking_obj.delete()
    return HttpResponseRedirect("/booking-list/")

def stu_register(request):
    ok = ""
    if request.POST:
        stu_id = request.POST.get("stu_id")
        stu_name = request.POST.get("stu_name")
        stu_phone = request.POST.get("stu_phone")
        stu_college = request.POST.get("stu_college")
        stu_class = request.POST.get("stu_class")
        
        if Student.objects.filter(stu_number__exact=stu_id).count() == 0:
            obj = Student.objects.create(
                stu_number=stu_id,
                stu_name=stu_name,
                stu_phone_number=stu_phone,
                stu_college=stu_college,
                stu_class=stu_class
            )
            obj.save()
            if obj.id:
                ok = "注册成功！"
            else:
                ok = "注册失败！"
        else:
            ok = "注册失败！"
    context = {
        "ok": ok
    }
    return render(request, "stu-register.html", context=context)

def logout(request):
    del request.session["code"]
    del request.session["username"]
    del request.session["access_token"]
    del request.session["yiban_id"]
    return HttpResponseRedirect("/index/")

@csrf_exempt
def index(request):
    student = YibanId()
    user = "登录"
    link = "/get_oauth/"

    if request.GET.get("code"):
        student.code = request.GET.get("code")
        # print("code = " + student.code)
        get_access_token_url = "https://openapi.yiban.cn/oauth/access_token"
        form_data = {
            "client_id": "<client_id>",
            "client_secret": "<secret_id>",
            "code": student.code,
            "redirect_uri": "<redirect_uri>",
        }
        re2 = requests.post(get_access_token_url, data=form_data)
        student.access_token = json.loads(re2.text).get("access_token")
        student.yiban_id = json.loads(re2.text).get("userid")
        
        request.session['code'] = student.code
        request.session["access_token"] = student.access_token
        request.session['yiban_id'] = student.yiban_id

        # print("access_token = " + student.access_token)
        if request.session.get("username"):
            user = request.session.get("username") + "，点击查看自己的预定"
            link = "/booking-list/"
        else:
            user_t = me(student.access_token).get("info").get("yb_username")
            request.session["username"] = user_t
            user = user_t + "，点击查看自己的预定"
            link = "/booking-list/"
        # print("after me")

    if request.session.get("username"):
        user = request.session.get("username") + "，点击查看自己的预定"
        link = "/booking-list/"
    else:
        user = "登录"
        link = "/get_oauth/"

    limit = 10
    info = Speech.objects.order_by('speech_add_time')
    
    paginator = Paginator(info, limit)
    page = request.GET.get('page', 1)
    loaded = paginator.page(page)

    context = {
        "all_title": "贵州大学讲座预登记系统",
        'ArticleInfo': loaded,
        "user": user,
        "link": link
    }
    return render(request, "index.html", context)

def debug(request):
    return render(request, "debug-msg.html", context={"msg": str(request.GET)})

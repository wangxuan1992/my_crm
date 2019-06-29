from django.urls import reverse
# from crm.templatetags import my_tags


def reverse_url(request,name,*args,**kwargs):

    next = request.GET.get('next')
    # next = request.get_full_path()
    # print(next,'--1')

    if next:
        ret = next
    else:
        ret = reverse(name,args=args,kwargs=kwargs)
    return ret
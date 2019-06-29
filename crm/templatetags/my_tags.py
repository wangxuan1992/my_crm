from django import template

register = template.Library()

from django.urls import reverse
from django.http.request import QueryDict


@register.simple_tag
def reverse_url(request, name, *args, **kwargs):
    base_url = reverse(name, args=args, kwargs=kwargs)
    next = request.get_full_path()
    # print(next)
    dic = QueryDict(mutable=True)
    dic['next'] = next
    # print(dic)
    return "{}?{}".format(base_url, dic.urlencode())

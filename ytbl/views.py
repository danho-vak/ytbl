from django.shortcuts import render

from django.http import HttpResponse

from . models import Coordinates
from django.db.models import Q
from django.core.serializers.json import DjangoJSONEncoder
import json


# Create your views here.

def showMap(request):
    cb_coordinates = ''
    type_code = request.GET.get('type_code')# type_code = 1:헌옷수거함, 2:폐건전지/형광등수거함 , default:모두
    if type_code == '1':
        cb_coordinates = Coordinates.objects.filter(type_code=1)
    elif type_code == '2':
        cb_coordinates = Coordinates.objects.filter(Q(type_code=2) | Q(is_next_to=True))
    else:
        # annotate한 attribute는 serialize가 되지 않는 이슈 발생
        cb_coordinates = Coordinates.objects.all()

    cb_coordinates_json = json.dumps(list(cb_coordinates.values()), ensure_ascii=False, cls=DjangoJSONEncoder)

    return render(request, 'ytbl/showMap.html', {'data':cb_coordinates_json})

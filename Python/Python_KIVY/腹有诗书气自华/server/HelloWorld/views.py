from django.http import HttpResponse
import json
from .DataGet import DataBase

def GetSort(request):
    request.encoding='utf-8'
    if 'top' in request.GET and request.GET['top']:
        top = int(request.GET['top'])
    else:
        top = 20
    result = DataBase().GetTop(top)

    return HttpResponse(json.dumps(result))

def GetIDSort(request):
    request.encoding='utf-8'
    if 'id' in request.GET and request.GET['id']:
        _id = int(request.GET['id'])
        result = DataBase().GetIdSort(_id)
        return HttpResponse(json.dumps(result))
    else:
        return HttpResponse(json.dumps({}))

def Register(request):
    request.encoding='utf-8'
    if 'username' in request.GET and request.GET['username']:
        name = request.GET['username']
        result = DataBase().AddUser(name)
        return HttpResponse(json.dumps(result))
    else:
        return HttpResponse(json.dumps({}))

def Update(request):
    request.encoding='utf-8'
    if 'num' in request.GET and request.GET['num'] and 'id' in request.GET and request.GET['id']:
        num = int(request.GET['num'])
        _id = int(request.GET['id'])
        result = DataBase().AlterNum(_id, num)
        return HttpResponse(json.dumps(result))
    elif 'username' in request.GET and request.GET['username'] and 'id' in request.GET and request.GET['id']:
        _id = int(request.GET['id'])
        name = request.GET['username']
        result = DataBase().AlterName(_id, name)
        return HttpResponse(json.dumps(result))
    else:
        return HttpResponse(json.dumps({}))


    
# Create your views here.
from django.db import connection
from django.db.models.aggregates import Sum
from django.http.response import HttpResponse
from django.template import loader
from django.template.context import RequestContext
import json
from dirvishserver.filetree import Filetree, FiletreeEncoder
from dirvishserver.models import Image, File, ImageFile


def index(request):
    t = loader.get_template("index.html")
    hosts = Image.objects.all().values('name').distinct()
    c = RequestContext(request, {'hosts': hosts})
    response = HttpResponse(t.render(c))
    response['Access-Control-Allow-Origin'] = '*'
    return response

def hosts(request):
    hosts = Image.objects.all().values('name').distinct()
    images = Image.objects.all().order_by('time')
    c = RequestContext(request, {'hosts': hosts, 'images': images})
    response_data = {}

    resp_host  = []
    for host in hosts:
        #resp_host.append({'name': host['name']})
        images = Image.objects.filter(name=host['name']).order_by('time')
        resp_image = []
        for image in images:
            resp_image.append({'name': image.time, 'id': image.id})
        resp_host.append({'name': host['name'], 'images': resp_image})


    response_data['hosts'] = resp_host

    response = HttpResponse(json.dumps(response_data), content_type="application/json")
    response['Access-Control-Allow-Origin'] = '*'
    return response
def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

def trend(request):
    host = request.GET.get('hostname')
    # values = ImageFile.objects.filter(image__name=host).annotate(Sum('size'))
    cursor = connection.cursor()
    cursor.execute("select sum(f.size) as sum, i.time as time, i.id as id from file f, image_file if, image i WHERE f.id = if.file_id AND if.image_id = i.id AND i.name = '" + host +"' AND f.type=0 GROUP BY i.id ORDER BY i.time")
    result = dictfetchall(cursor)
    # sql select sum(f.size), i.time from file f, image_file if, image i WHERE f.id = if.file_id AND if.image_id = i.id AND i.name = 'fs1' GROUP BY i.id;
    c = RequestContext(request, {'host': host, 'values': result})

    response_data = {'host': host, 'images':result}

    response = HttpResponse(json.dumps(response_data), content_type="application/json")
    response['Access-Control-Allow-Origin'] = '*'
    return response

def topx(request):
    host = request.GET.get('hostname')
    image = request.GET.get('image')
    size = request.GET.get('size', 50)

    # values = ImageFile.objects.filter(image__name=host).annotate(Sum('size'))
    cursor = connection.cursor()
    # select f.name, f.size from file f, image_file if WHERE f.id = if.file_id AND if.image_id = 2 AND f.type=0 ORDER BY f.size DESC LIMIT 50;
    cursor.execute("select f.name as name, f.size as size from file f, image_file if WHERE f.id = if.file_id AND if.image_id = " + str(image) + " AND f.type=0 ORDER BY f.size DESC LIMIT " + str(size) + ";")
    result = dictfetchall(cursor)
    # sql select sum(f.size), i.time from file f, image_file if, image i WHERE f.id = if.file_id AND if.image_id = i.id AND i.name = 'fs1' GROUP BY i.id;
    response_data = {'host': host, 'files':result}

    response = HttpResponse(json.dumps(response_data), content_type="application/json")
    response['Access-Control-Allow-Origin'] = '*'
    return response

def detail(request):
    host = request.GET.get('hostname')
    image = request.GET.get('image')

    files = File.objects.raw("SELECT * from file f, image_file if WHERE f.id = if.file_id AND if.image_id=" + image + " AND f.type = 0 ORDER BY f.name;")
    tree = Filetree('', '/',0)
    for file in files:
        tree.append(file.name, file.size)
    response = HttpResponse(FiletreeEncoder().encode(tree), content_type="application/json")
    response['Access-Control-Allow-Origin'] = '*'
    return response

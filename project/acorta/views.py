from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from models import UrlsList
from django.views.decorators.csrf import csrf_exempt

def createLink(string):
    link = '<table border="2px" style="background:#B294AC">'
    link += "<tr>"
    link += "<td>" + string + "</td>"
    link += "</tr>"
    link += "</table>"
    return link
    
    
def createTable(list1, list2):
	table = '<table border="5px" style="background:#B294AC">'
	table += "<tr>"
	table += "<td>URL ORIGINAL</td>"
	table += "<td>URL ACORTADA</td>"
	table += "</tr>"
	table += "<tr>"
	table += "<td>" + list1 + "</td>"
	table += "<td>" + list2 + "</td>"
	table += "</tr>"
	table += "</table>"
	return table

def extractUrl(body):
    url = body.split("=")[1]
    if len(url.split("%3A%2F%2F")) == 1:
		if url != "":
			url = "http://" + url
    else:
        url = url.replace("%3A%2F%2F", "://")
    return url

def getNumUrls():
    tableDB = UrlsList.objects.all()
    if len(tableDB) == 0:
        num = 0
    else:
        num = len(tableDB)
    numUrls = num
    return numUrls

@csrf_exempt

def getForm(request):
    method = request.method
    form = ""
    if method == "GET":
        form += "<html><body>" 
        form += '<body style="background:#5C0349">'
        form += '<span style="color:#FCF8FA">'
        form += '<form action=""method="POST">'
        form += "<p><h1>ACORTADOR DE URLS</h1></p>"
        form += '<h4>Introduce una Url para acortar -> <input type="text" name="url"</h4>'
        form += '<input type="submit">'
        form += '</form>'
        form += "</body></html>"
        
        numUrls = getNumUrls()
        if (numUrls > 0):
            tableDB = UrlsList.objects.all()
            urlStock = ""
            shortedUrlStock = ""
            for line in tableDB:
                urlStock += "<p>" + line.url + "</p>"
                shortedUrlStock += "<p>" + line.shortedUrl + "</p>"
            table = createTable(urlStock, shortedUrlStock)
            form += "<html><body>"
            form += "<h3>Lista de urls:</h3>"
            form += table
            form += "</body></html>"
        
    elif method == "POST":
        url = extractUrl(request.body)
        tableDB = UrlsList.objects.all()
        numUrls = getNumUrls()
        found = False
        for line in tableDB:
            urlDB = line.url
            if url == urlDB:
                found = True
        if not found:
            shortedUrl = "http://localhost:1234/" + str(numUrls)
            entry = UrlsList(url=url, shortedUrl=shortedUrl)
            entry.save()
            numUrls = numUrls + 1
            
        shortedUrlDB = (UrlsList.objects.get(url=url)).shortedUrl
        link = createLink("VOLVER")
        linkUrl = createLink(url)
        linkShortedUrl = createLink(shortedUrlDB)
        clickable = '<p><h4><a style="color:#FCF8FA"' + "href='" + url + "'>Url" + linkUrl + "</a></h4></p>"
        clickable += '<p><h4><a style="color:#FCF8FA"' + "href='" + url + "'>Url acortada" + linkShortedUrl + "</a></h4></p>"
        clickable += "<p><a href='http://localhost:1234/'>" + link + "</a></p>"
        form = '<html><body style="background:#5C0349">' + clickable + "</body></html>"
	
    return HttpResponse(form)
	
def getUrl(request, attribute):
    shortedUrl = "http://localhost:1234/" + str(attribute)
    verb = request.method
    form = ""
    if verb == "GET":
        try:
            url = (UrlsList.objects.get(shortedUrl=shortedUrl)).url
            form += "<html><head><meta http-equiv=Refresh content= 0;url=" + url + "></head></body></html>"
        except UrlsList.DoesNotExist:
            link = createLink("VOLVER")
            form += "<p>ERROR: la url introducida no esta disponible</p>"
            form += "<p><a href='http://localhost:1234/'>" + link + "</a></p>"
            return HttpResponseNotFound(form)
    return HttpResponse(form)

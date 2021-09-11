from django.urls import path

from rest_framework.decorators import api_view
from rest_framework.response import Response
import os

from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import PDFPageAggregator
from pdfminer3.converter import TextConverter
import io

def readPdf():
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    with open('name.pdf', 'rb') as fh:

        for page in PDFPage.get_pages(fh,
                                    caching=True,
                                    check_extractable=True):
            page_interpreter.process_page(page)

        text = fake_file_handle.getvalue()

    # close open handles
    converter.close()
    fake_file_handle.close()

    newArr = []
    splits = text.split("\n")
    for i in range(len(splits)):
        if(splits[i] != ""):
            newArr.append(splits[i])
    return newArr

def getName(newa):
    for i in range(len(newa)):
        if(newa[i] == "\xa0"):
            return [newa[i+3],newa[i+4]]
def getTopSkills(newa):
    for i in range(len(newa)):
        if(newa[i] == "Top Skills"):
            return {newa[i+1],newa[i+2], newa[i+3]}

def getContactNumber(newa):
    for i in range(len(newa)):
        if(newa[i][-6:] == "(Home)"):
            return newa[i] 


def handle_uploaded_file(f):
    with open('name.pdf', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

@api_view(['POST'])
def returnSomeThing(request):
    handle_uploaded_file(request.data["file"])
    pdf = readPdf()
    
    os.remove("name.pdf")
    name = getName(pdf)
    return Response({
        "name": name[0],
        "tag": name[1],
        "skills" :getTopSkills(pdf),
        "contactNumber": getContactNumber(pdf),
    })

urlpatterns = [
    path("", returnSomeThing)
]
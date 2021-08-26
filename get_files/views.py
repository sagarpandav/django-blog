from django.shortcuts import render
from rest_framework.decorators import api_view
import os
import json
from bson import ObjectId, datetime
from django.http import JsonResponse, HttpResponse
from django.http import FileResponse
import datetime
from datetime import date
from collections import OrderedDict

import logging
import boto3
import io
import base64
import tempfile



from .env_secrets import aws_env

#CONSTANTS
BUCKET_DIR = aws_env['bucket_dir']
AWS_ACCESS_KEY = aws_env['aws_access_key']
AWS_SECRET_KEY = aws_env['aws_secret_key']
AWS_BUCKET_NAME = aws_env['aws_bucket_name']


class JSONEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, ObjectId) or isinstance(o, (datetime.date, datetime.datetime)):
            return str(o)
        return json.JSONEncoder.default(self, o)

# Create your views here.
@api_view(['POST'])    
def get_filename(request):
    try: 
        print("Enter Try++++++++++++++++++", request)
        file_name = request.POST["file_name"]
        print("File_name++++++++++++++", file_name)
        os.system("bash get_files/search_script.sh "+ file_name)

        file_path = 'get_files/'+file_name
        print(file_path)
        file_result = FileResponse(open(file_path, 'rb'))
        print(type(file_result))
        json_result = {"FILE_NAME": file_name}
        # json_result = JSONEncoder().encode({"FILE_NAME": file_name})
        print("JSON",json_result)
        # return JsonResponse(json_result, safe=False)
        return file_result

    except Exception as error:
        print("error in get filename string",error)
        # LOGGER.exception(error)

@api_view(['POST'])
def upload_file(request):
    try:
        # logging.debug("Enter GET FILE FUNCTION")
        print("Enter GET FILE FUNCTION")
        fileToUpload = request.FILES.get('file')
        cloudFilename = BUCKET_DIR + fileToUpload.name 
        
        # logging.info(cloudFilename)
        print('cloudFilename: ',cloudFilename)

        s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY,aws_secret_access_key=AWS_SECRET_KEY)
        s3_client.upload_fileobj(fileToUpload, AWS_BUCKET_NAME, cloudFilename)
        print("Upload done: ", fileToUpload.name)


        # session = boto3.session.Session(aws_access_key_id=AWS_ACCESS_KEY,
        #                                 aws_secret_access_key=AWS_SECRET_KEY)
        # s3 = session.resource('s3')
        # s3.Bucket(AWS_BUCKET_NAME).put_object(Key=cloudFilename, Body=fileToUpload)
        json_result = {"cloudFilename": cloudFilename}
        return JsonResponse(json_result, safe=False)

    except Exception as error:
        logging.error(error)


@api_view(['POST'])
def download_file(request):
    try:
        print("ENTER DOWNLOAD FILE FUNCTION")
        file_name = request.POST['file_name']
        cloudFilename = BUCKET_DIR + file_name

        print('cloudFilename: ', cloudFilename)

        s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
        
        # tmp = tempfile.NamedTemporaryFile()
        # with open(tmp.name, 'wb') as file_obj:
        #     s3_client.download_fileobj(AWS_BUCKET_NAME, cloudFilename, file_obj)

        tmp = tempfile.NamedTemporaryFile(mode='w', delete=False)
        with open(tmp.name, 'wb') as file_obj:
            s3_client.download_fileobj(AWS_BUCKET_NAME, cloudFilename, file_obj)

        print("file_obj: ",  file_obj)
        print("TYPE OF file_obj: ", type(file_obj))

        tmp.close()
        os.remove(tmp.name)


        # file_base64 = base64.b64encode(file_stream)

        json_result = {file_name: str(file_obj)}
        return JsonResponse(json_result, safe=False)

        # return HttpResponse(str(file_stream), 'image/jpeg')

    except Exception as error:
        logging.error(error)
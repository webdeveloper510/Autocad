from django.shortcuts import render
from django.http import HttpResponse
from shading3dmodel.models import *
from shading3dmodel.serializers import *
from shading3dmodel.renderer import UserRenderer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate
from distutils import errors
import cv2
from .test import read_three_component, create_pdf  # Import your custom functions from test.py
from urllib.parse import urljoin
from . autocad import generate_images
import numpy as np
import subprocess
import os 
# url="http://127.0.0.1:8000/static/media/"
url="http://18.234.253.236:8000/static/media/"

os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = '/home/codenomad/anaconda3/envs/newpyoccenv/lib/python3.11/site-packages(from PyQt5) (12.13.0)'

def get_tokens_for_user(user):
    refresh=RefreshToken.for_user(user)
    return {
        'access':str(refresh.access_token)
    }
    
class UserRegistrationView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        serializer=UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            return Response({'message':'Registation successful',"status":"status.HTTP_200_OK",'user_id': user.id})
        return Response({errors:serializer.errors},status=status.HTTP_400_BAD_REQUEST)
class UserLoginView(APIView):
    renderer_classes=[UserRenderer]
    
    def post(self,request,format=None):
        serializer=UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email=serializer.data.get('email')
        password=serializer.data.get('password')
        
        user=authenticate(email=email,password=password)
        if user is not None:
            token=get_tokens_for_user(user)
            is_admin=user.is_staff
            return Response({'token':token, "is_admin":is_admin,'msg':'Login Success'}, status=status.HTTP_200_OK)
        else:
            return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)
        
class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    authentication_classes=[JWTAuthentication]
    def get(self, request, format=None):
        try:
            serializer = UserProfileSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AutocadAnalysesView(APIView):
    authentication_classes=[JWTAuthentication]
    
    def post(self, request, format=None):
        step_file=request.FILES.get("step_file")
        if not step_file:
            return Response({"message": "File Must Required"}, status=status.HTTP_404_NOT_FOUND)
        
        stp_ID = ''
        if step_file:
            file_save=FileData.objects.create(stpfile=step_file,filename=step_file.name)
            serializer=FileDataSerializer(data=file_save)
            file_save.save()
            full_url = urljoin(url, file_save.stpfile.name)
            file_path=file_save.stpfile.path
            file_save.stpfile = full_url
            file_save.save()
            stp_ID = file_save.id
            step_file=file_path
            generate_images(file_path=step_file)
            
        # Execute the demo_new.py script using subprocess
        command = ["/home/codenomad/anaconda3/envs/newpyoccenv/bin/python", os.getcwd()+"/shading3dmodel/autocad.py", ]
        try:
            result = subprocess.run(command, capture_output=True, text=True)
            input_dir = os.getcwd()+"/static/screenshot"  # Define the input directory path
            pdf_output = os.getcwd()+"/static/media//pdf_dir/autocad.pdf"  # Define the PDF output path
            all_images = read_three_component(input_dir)
            pdf_output=create_pdf(all_images, pdf_output)
            pdf_name=pdf_output.split("//")[-1]
            pdf_url=urljoin(url,pdf_name )
            if stp_ID:
                file_data = FileData.objects.get(id=stp_ID)
                file_data.pdffile = pdf_url
                file_data.save()

            # Check if the script executed successfully
            if result.returncode != 0:
                # Script encountered an error; return the error message
                return Response({"error": result.stderr}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"message": "Script executed successfully!",}, status=status.HTTP_200_OK)
    
class CSVFileGEt(APIView):
    def get(self,request,format=None):
        filedata=FileData.objects.all().values().order_by('-id')
        return Response({'data':filedata},status=status.HTTP_200_OK)
from django.shortcuts import render
from rest_framework.views import APIView
from .models import Products
from .serializers import ProductsSerializer
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class ProductView(APIView):
    def get(self, request):
        product = Products.objects.all()
        serializer = ProductsSerializer(product,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer = ProductsSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message':"Product Added Successfully ",
                'data':serializer.data
            },status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status= status.HTTP_400_BAD_REQUEST)
    

class ProductDetialView(APIView):
    def get_object(self,pk):
        return Products.objects.get(pk=pk)
    
    def get(self,request,pk):
        product = self.get_object(pk)
        serializer = ProductsSerializer(product)
        return Response(serializer.data)
    
    def put(self,request,pk):
        product = self.get_object(pk)
        serializer = ProductsSerializer(product,data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Updated Successfully !'})
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        product = self.get_object(pk)
        product.delete()
        return Response({'message':'Deleted Successfully !'})
    
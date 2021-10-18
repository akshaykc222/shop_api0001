from rest_framework import viewsets

from .serializer import *
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


class CategoryView(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def get(self, request):
        queryset = SubCategory.objects.all()
        serializer = SubCategorySerializer(queryset, many=True)
        return Response({"Categories": serializer.data})


class SubCategoryView(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def get(self, request, pk):
        queryset = SubCategory.objects.filter(id=pk)
        serializer = SubCategorySerializer(queryset, many=True)
        return Response(serializer.data)


class ProductView(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def get(self, request, pk):
        query = Product.objects.filter(id=pk)
        data = []
        serializer_context = {
            'request': request,
        }

        serializer = ProductSerializer(query, many=True, context=serializer_context)
        for product in serializer.data:
            fab_query = Favourite.objects.filter(user=request.user).filter(product=product['id'])
            if fab_query:
                product['isFavourite'] = fab_query[0].isFavourite
            else:
                product['isFavourite'] = False
            data.append(product)
        return Response({"Products": data})


class FavouriteView(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def post(self, request):

        product = request.data["id"]
        try:
            product_obj = Product.objects.get(id=product)
            user = request.user
            single_favourite_product = Favourite.objects.filter(user=user).filter(product=product_obj).first()
            if single_favourite_product:
                print("single_favorit_product")
                ccc = single_favourite_product.isFavourite
                single_favourite_product.isFavourite = not ccc
                single_favourite_product.save()
            else:
                Favourite.objects.create(
                    product=product_obj, user=user, isFavourite=True)

            response_msg = {'error': False}

        except Exception as e:
            print("something went wrong " + str(e))
            response_msg = {'error': True}
        return Response(response_msg)


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"error": False})
        return Response({"error": True})

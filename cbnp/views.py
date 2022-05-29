from tempfile import NamedTemporaryFile

from django.db.utils import IntegrityError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Product
from .serializers import (
    ClientSerializer,
    ProductSerializer,
    MyTokenObtainPairSerializer,
    SignInSerializer,
    FileSerializer,
)

import pandas as pd

from sqlite3 import IntegrityError

from .customsql.querys import (
    read_clients,
    create_clients,
    update_clients,
    delete_clients,
    join_tables
)


def error_response(exception):
    return Response(
        {'status': 'error', 'data': f'{exception}'},
        status=500,
        content_type='application/json'
    )


def parse_db_client(client):
    client = {
        'id': client[0],
        'email': client[1],
        'document': client[2],
        'first_name': client[3],
        'last_name': client[4],
    }
    return client


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class ViewSignUp(APIView):
    """
    ViewSignIn
    """

    def post(self, request):
        """
        post
        """
        data = request.data
        data['username'] = data['email']
        signin = SignInSerializer(data=request.data)
        signin.is_valid(raise_exception=True)
        signin.save()

        return Response(
            signin.data,
            status=201,
            content_type='application/json'
        )


class ViewClient(APIView):
    """
    list_clients
    """

    permission_classes = [IsAuthenticated]


    def get(self, request: object) -> Response:
        """
        Request GET method
        :rtype: Response
        :param request: HTTP request values
        :return: HttpResponse
        """
        id = request.query_params.get('id')
        try:
            parse_clients = []
            clients = read_clients(id=id if id else None)
            for client in clients:
                client = parse_db_client(client)
                parse_clients.append(client)
            serializer = ClientSerializer(parse_clients, many=True)
            return Response(
                serializer.data,
                status=200,
                content_type='application/json'
            )
        except Exception as e:
            response = error_response(e)

        return Response(
            response,
            status=200,
            content_type='application/json'
        )

    def post(self, request: object) -> Response:
        """
        Request POST method
        :rtype: Response
        :param request: HTTP request values
        :return: HttpResponse
        """
        try:
            data = request.data

            if data.get('create', ''):
                serializer = ClientSerializer(data=data['create'])
                serializer.is_valid(raise_exception=True)
                client = create_clients(**serializer.data)
                client = {
                    'id': client
                    ** serializer.data,
                }
            elif data.get('update', ''):
                client = update_clients(**data['update'])
                client = {
                    'id': client,
                    **data['update'],
                }
            elif data.get('delete', ''):
                client = delete_clients(**data['delete'])
                if not client:
                    return Response(
                        {'status': 'error', 'data': 'Client not found'},
                        status=404,
                        content_type='application/json'
                    )
                client = {
                    'id': client,
                    **data['delete'],
                }

            return Response(
                client,
                status=201,
                content_type='application/json'
            )
        except Exception as e:
            return error_response(e)


class viewFileClients(APIView):
    """
    files_clients
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Request GET method
        :rtype: Response
        :param request: HTTP request values
        :return: HttpResponse
        """
        id = request.query_params.get('id')
        params = {
            'clients': 'id',
            'bills': 'client_id',
        }
        table = join_tables(params, id=id if id else None)

        table = pd.DataFrame(table, columns=['id', 'email', 'document', 'first_name',
                             'last_name', 'bill_id', 'client_id', 'company_name', 'nit', 'code'])

        with NamedTemporaryFile(suffix='.csv',) as file:
            table.to_csv(file.name, index=False)
            file.seek(0)
            response = Response(file.read(), status=200,
                                content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="clients.csv"'
            return response

    def post(self, request):
        """
        Request POST method
        :rtype: Response
        :param request: HTTP request values
        :return: HttpResponse
        """

        file = FileSerializer(data=request.data)
        file.is_valid(raise_exception=True)

        df = pd.read_csv(file.validated_data['file'])
        columns = []
        clients = []
        for col in df:
            columns.append(col)
        for i in df.index:
            try:
                client = {}
                client[columns[0]] = df.loc[i, columns[0]]
                client[columns[1]] = df.loc[i, columns[1]]
                client[columns[2]] = df.loc[i, columns[2]]
                client[columns[3]] = df.loc[i, columns[3]]
                serializer = ClientSerializer(data=client)
                serializer.is_valid(raise_exception=True)
                client = create_clients(**serializer.data)
                client = {
                    'id': client,
                    **serializer.data,
                }
                clients.append(client)
            except IntegrityError:
                clients.append(
                    {'error': 'Client already exists', **serializer.data, })

        return Response(
            clients,
            status=201,
            content_type='application/json'
        )


class ViewProduct(APIView):
    """
    list_products
    """

    permission_classes = [IsAuthenticated]

    def get(self, request: object) -> Response:
        """
        Request GET method
        :rtype: Response
        :param request: HTTP request values
        :return: HttpResponse
        """
        id = request.query_params.get('id')
        try:
            if not id:
                product = Product.objects.all()
                product = ProductSerializer(product, many=True)
            else:
                product = Product.objects.get(id=id)
                product = ProductSerializer(product)
            response = Response(
                product.data,
                status=200,
                content_type='application/json'
            )
        except Product.DoesNotExist:
            response = Response(
                {'status': 'error', 'data': f'Product {id} not found'},
                status=404,
                content_type='application/json'
            )
        except Exception as e:
            response = error_response(e)

        return response

    def post(self, request: object, id=None) -> Response:
        """
        Request POST method
        :rtype: Response
        :param request: HTTP request values
        :return: HttpResponse
        """

        try:
            product = ProductSerializer(data=request.data)
            if product.is_valid():
                product = Product(**product.validated_data)
                product.save()
                response = Response(
                    {'product_id': product.id, 'product_name': product.name},
                    status=201,
                    content_type='application/json'
                )
            else:
                response = Response(
                    {'status': 'error', 'data': product.errors},
                    status=200,
                    content_type='application/json'
                )

        except IntegrityError as e:
            response = Response(
                {'status': 'error', 'data': f'el producto ya existe'},
                status=418,
                content_type='application/json'
            )
        except Exception as e:
            response = error_response(e)

        return response

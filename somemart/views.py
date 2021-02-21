import json

from django.contrib.auth import authenticate
from django.http import HttpResponse, JsonResponse, Http404
from django.views import View
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Item, Review
from base64 import b64decode

ADD_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {
            "type": "string",
            "minLength": 1,
            "maxLength": 64
        },
        "description": {
            "type": "string",
            "minLength": 1,
            "maxLength": 1024
        },
        "price": {
            "anyOf": [
                {"type": "string",
                 "pattern": "^\d+$"
                 },
                {
                    "type": "number",
                    "minimum": 1,
                    "maximum": 1000000
                }
            ]
        },
    },
    "required": ["title", "description", "price"],
}

POST_SCHEMA = {
    "type": "object",
    "properties": {
        "text": {
            "type": "string",
            "minLength": 1,
            "maxLength": 1024
        },
        "grade": {
            "anyOf": [
                {"type": "string",
                 "pattern": "^\d+$"
                 },
                {
                    "type": "number",
                    "minimum": 1,
                    "maximum": 10
                }
            ]
        },
    },
    "required": ["text", "grade"],
}

@method_decorator(csrf_exempt, name='dispatch')
class AddItemView(View):
    """View для создания товара."""

    def post(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION')
        if auth is None:
            return HttpResponse('', status=401)
        auth_data = b64decode(auth).decode('ascii').split(':')
        login = auth_data[0]
        password = auth_data[1]
        user = authenticate(username=login, password=password)
        if user is None:
            return HttpResponse('', status=401)
        if not user.is_staff:
            return HttpResponse('', status=403)
        try:
            document = json.loads(request.body)
            validate(document, ADD_SCHEMA)
            i = Item.objects.create(title=document['title'],
                                    description=document['description'],
                                    price=int(document['price']))
            i.save()
            return JsonResponse({'id': i.id}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'errors': 'Invalid JSON'}, status=400)
        except ValidationError as exc:
            return JsonResponse({'errors': exc.message}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class PostReviewView(View):
    """View для создания отзыва о товаре."""

    def post(self, request, item_id):
        try:
            i = Item.objects.get(pk=item_id)
        except Item.DoesNotExist:
            raise Http404
        try:
           document = json.loads(request.body)
           validate(document, POST_SCHEMA)
           r = Review.objects.create(text=document['text'],
                                     grade=document['grade'],
                                     item=i)
           r.save()
           return JsonResponse({'id': r.id}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'errors': 'Invalid JSON'}, status=400)
        except ValidationError as exc:
            return JsonResponse({'errors': exc.message}, status=400)


class GetItemView(View):
    """View для получения информации о товаре.

    Помимо основной информации выдает последние отзывы о товаре, не более 5
    штук.
    """

    def get(self, request, item_id):
        try:
            i = Item.objects.get(pk=item_id)
        except Item.DoesNotExist:
            raise Http404
        queryset = Review.objects.filter(item=i)
        if queryset.count() > 5:
            reviews = queryset.order_by('-pk')[:5]
        else:
            reviews = queryset
        reviews_list = []
        for r in reviews:
            r_data = {
                "id": r.id,
                "text": r.text,
                "grade": r.grade
            }
            reviews_list.append(r_data)
        query_data = {
            "id": i.id,
            "title": i.title,
            "description": i.description,
            "price": i.price,
            "reviews": reviews_list,
        }
        return JsonResponse(query_data, status=200)



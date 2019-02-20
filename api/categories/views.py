from django.http import JsonResponse, HttpRequest
from categories.models import Category
import json
from api_utils.views_utils import get_category_names, validate_data

from django.views.decorators.csrf import csrf_exempt


def get(request: HttpRequest):
    pk = request.GET.get('id')

    category = Category.objects.get(pk=pk)

    category_serialized = {'id': category.pk, 'name': category.name}
    parents_serialized = [{'id': parent.id, 'name': parent.name} for parent in Category.get_parents(pk)]
    children_serialized = [{'id': child.id, 'name': child.name} for child in Category.get_children(pk)]
    siblings_serialized = [{'id': sibling.id, 'name': sibling.name} for sibling in Category.get_siblings(pk)]

    result = category_serialized

    result.update({'parents': parents_serialized})
    result.update({'children': children_serialized})
    result.update({'sibling': siblings_serialized})

    return JsonResponse(result)


@csrf_exempt  # for debugging
def post(request):
    failed_categories = []

    if request.method == 'POST':
        result = {
            'status': 'Created',
            'code': 201
        }

        data = json.loads(request.POST['result'], encoding='utf-8')

        if not validate_data(data):
            result['status'] = 'Bad Request'
            result['code'] = 400
            return JsonResponse(result)

        category_names = get_category_names(data)

        for category in category_names:
            _, created = Category.objects.get_or_create(name=category)
            if not created:
                failed_categories.append(category)

        if len(failed_categories) < len(category_names):
            result.update({'existing categories': failed_categories})
        else:
            result['status'] = 'Accept'
            result['code'] = 202

        return JsonResponse(result)

    return JsonResponse({'error': 'only POST method is allowed'})

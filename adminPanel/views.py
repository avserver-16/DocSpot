from django.http import JsonResponse
from tweet.models import Tweet

def search_suggestions(request):
    query = request.GET.get('query', '').lower()
    if not query:
        return JsonResponse([], safe=False)
    
    files = Tweet.objects.filter(name__icontains=query)
    suggestions = [
        {
            'name': file.name,
            'url': file.file.url if file.file else None
        }
        for file in files
    ]
    return JsonResponse(suggestions, safe=False)
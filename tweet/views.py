from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Count
from .models import Tweet
from .forms import TweetForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import UserRegistrationForm
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.db.models import Q

User = get_user_model()

class TweetListView(ListView):
    model = Tweet
    template_name = 'tweet_list.html'
    context_object_name = 'tweets'
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get('category')
        search_query = self.request.GET.get('search')
        
        if category and category != 'all':
            if category == 'other':
                queryset = queryset.filter(category='other')
            else:
                queryset = queryset.filter(category=category)
        
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        
        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get all tweets for the search functionality in base template
        context['all_tweets'] = Tweet.objects.all().order_by('-created_at')
        
        # Get category statistics
        category_stats = Tweet.objects.values('category').annotate(
            count=Count('id')
        ).order_by('category')
        
        total_docs = Tweet.objects.count()
        category_percentages = []
        
        for stat in category_stats:
            percentage = (stat['count'] / total_docs * 100) if total_docs > 0 else 0
            category_percentages.append({
                'category': dict(Tweet.CATEGORY_CHOICES).get(stat['category'], 'Other'),
                'count': stat['count'],
                'percentage': round(percentage, 1)
            })
        
        context['category_stats'] = category_percentages
        return context

class TweetCreateView(LoginRequiredMixin, CreateView):
    model = Tweet
    form_class = TweetForm
    template_name = 'tweet_form.html'
    success_url = reverse_lazy('tweet_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        # Handle custom category when 'other' is selected
        if form.cleaned_data['category'] == 'other' and form.cleaned_data['custom_category']:
            form.instance.custom_category = form.cleaned_data['custom_category']
        return super().form_valid(form)

class TweetUpdateView(LoginRequiredMixin, UpdateView):
    model = Tweet
    form_class = TweetForm
    template_name = 'tweet_form.html'
    success_url = reverse_lazy('tweet_list')

    def form_valid(self, form):
        # Handle custom category when 'other' is selected
        if form.cleaned_data['category'] == 'other' and form.cleaned_data['custom_category']:
            form.instance.custom_category = form.cleaned_data['custom_category']
        elif form.cleaned_data['category'] != 'other':
            form.instance.custom_category = None  # Clear custom category if not 'other'
        return super().form_valid(form)

class TweetDeleteView(LoginRequiredMixin, DeleteView):
    model = Tweet
    template_name = 'tweet_confirm_delete.html'
    success_url = reverse_lazy('tweet_list')

def index(request):
    return render(request,'index.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request,user)
            return redirect('tweet_list')
    else:
        form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})

def list_user_details():
    """Function to list all user details including sap_id."""
    users = User.objects.all()
    for user in users:
       
        print(f"{user .username} - {user.email}")  # Print username, email, and sap_id

def search_documents(request):
    query = request.GET.get('q', '')
    if len(query) < 2:
        return JsonResponse({'results': []})

    results = Tweet.objects.filter(
        Q(name__icontains=query) | 
        Q(category__icontains=query) |
        Q(custom_category__icontains=query)
    )[:5]  # Limit to 5 results

    documents = []
    for doc in results:
        documents.append({
            'id': doc.id,
            'name': doc.name,
            'category_display': doc.get_category_display_name(),
            'url': doc.file.url
        })

    return JsonResponse({'results': documents})

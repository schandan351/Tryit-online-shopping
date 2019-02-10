from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import Q
from products.models import Product



class SearchProductView(ListView):
    template_name="search/view.html"
    
    def get_queryset(self,*args,**kwargs):
        request=self.request
        print(request.GET)
        query=request.GET.get('q')
        print(query)
        if query is not None:
            # lookups=Q(title__icontains=query)|Q(description__icontains=query)
            return Product.objects.search(query)
        return Product.objects.none()

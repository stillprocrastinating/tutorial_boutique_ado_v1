from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render, reverse
from .models import Category, Product


def all_products(request):
    """
    A view to show all products, including sorting and search queries.
    """

    products = Product.objects.all()
    query = None
    categories = None

    if request.GET:
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']

            if not query:
                messages.error(
                    request, "You didn't enter any search criteria!"
                )
                return redirect(reverse('products'))

            queries = Q(
                name__icontains=query
            ) | Q(
                description__icontains=query
            )
            products = products.filter(queries)

    context = {
        'current_categories': categories,
        'products': products,
        'search_term': query,
    }
            
    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """
    A view to show individual product details.
    """

    product = get_object_or_404(Product, pk=product_id)

    return render(
        request, 'products/product_detail.html', {'product': product, }
    )

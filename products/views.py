from django.shortcuts import get_object_or_404, render
from .models import Product


def all_products(request):
    """
    A view to show all products, including sorting and search queries.
    """

    products = Product.objects.all()

    return render(request, 'products/products.html', {'products': products, })


def product_detail(request, product_id):
    """
    A view to show individual product details.
    """

    product = get_object_or_404(Product, pk=product_id)

    return render(
        request, 'products/product_detail.html', {'product': product, }
    )

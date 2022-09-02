from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .models import Category, Product, ReviewRating
from .forms import ReviewForm



def categories(request):
    return {
        'categories': Category.objects.all()
    }


def product_all(request):
    products = Product.objects.all()
    return render(request, 'store/main.html', {'products': products})


def product_detail(request, slug):

    product = get_object_or_404(Product, slug=slug, in_stock=True)
    reviews = ReviewRating.objects.filter(product=product).order_by('-udated_at')
    return render(request, 'store/products/detail.html', {'product': product, 'reviews': reviews})
    

def category_list(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(request, 'store/products/category.html', {'category': category, 'products': products})

#......................
def submit_review(request, pk):
    url = request.META.get('HTTP_REFERER')
    product = Product.objects.get(pk=pk)
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, pk=pk)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            
            return redirect('store:product_detail', slug=product.slug)

        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = pk
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect('store:product_detail', slug=product.slug)



    



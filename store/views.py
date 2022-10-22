from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Category, Product, ReviewRating
from .forms import ReviewForm, AddProduct
from cloudinary import uploader


def categories(request):
    return {
        'categories': Category.objects.all()
    }


def product_all(request):
    products = Product.objects.all()

    context = {
        'products': products,
        'is_admin': request.user.is_authenticated and request.user.is_superuser,
    }
    return render(request, 'store/main.html', context)


def product_detail(request, slug):

    product = get_object_or_404(Product, slug=slug, in_stock=True)
    reviews = ReviewRating.objects.filter(
        product=product).order_by('-udated_at')
    return render(request, 'store/products/detail.html',
                  {'product': product, 'reviews': reviews})


def category_list(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(request, 'store/products/category.html',
                  {'category': category, 'products': products})


# ADD PRODUCT....
@login_required
def add_product(request):
    if not request.user.is_superuser:
        # Redirect back to homepage if not a superuser
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('store:product_all'))

    if request.method == 'POST':
        form = AddProduct(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user
            product.save()
            messages.success(request, f'{product.title} Successfully Added!')
            return redirect(reverse('store:product_detail', args=[product.slug]))
        else:
            messages.error(request, 'Opps! Please ensure the form is valid.')
    else:
        form = AddProduct()

    template = 'store/products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


# EDIT PRODUCT
@login_required
def edit_product(request, product_id):
    """ Edit a product to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that!')
        return redirect(reverse('store:product_all'))

    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        form = AddProduct(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(
                request, f'{product.title}"Successfully edited product')
            return redirect(reverse('store:product_detail', args=[product.slug]))
        else:
            messages.error(request, 'Failed to edit product. Please ensure \
                the form is valid.')
    else:
        form = AddProduct(instance=product)

    template = 'store/products/edit_product.html'
    context = {'form': form, 'product': product}
    return render(request, template, context)


# DELETE PRODUCT
@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that!')
        return redirect(reverse('store:product_all'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        uploader.destroy(product.image.public_id)
        product.delete()
        messages.success(request, 'Product deleted!')

        return redirect(reverse('store:product_all'))
    return render(request, 'store/products/confirm_delete.html')

     # REVIEWS


def submit_review(request, pk):
    url = request.META.get('HTTP_REFERER')
    product = Product.objects.get(pk=pk)
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, pk=pk)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(
                request, 'Thank you! Your review has been updated.')

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
                messages.success(
                    request, 'Thank you! Your review has been submitted.')
                return redirect('store:product_detail', slug=product.slug)

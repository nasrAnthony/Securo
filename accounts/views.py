from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden, HttpResponseNotAllowed
from .forms import CustomUserCreationForm, CustomUserLoginForm, QuoteForm
from django.db.models import Count, Q
from .models import Quote

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
    else:
        form = CustomUserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')


def quote_request_view(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)

            if request.user.is_authenticated:
                quote.user = request.user

            quote.save()
            return redirect('home')
    else:
        form = QuoteForm()

    return render(request, 'quote_form.html', {'form': form})

@login_required
def profile_view(request):
    user = request.user
    quotes = Quote.objects.filter(email=user.email) | Quote.objects.filter(user=user)
    quotes = quotes.distinct().order_by('-submitted_at')  # Avoid duplicates if both filters match

    agg = quotes.aggregate(
    total=Count('id'),
    # If you have legacy data with "expired", treat it as cancelled too.
    cancelled=Count('id', filter=Q(status='cancelled') | Q(status='expired')),
    completed=Count('id', filter=Q(status='completed')),
    active=Count('id', filter=Q(status='active')),
    )

    # Your rule: “Open” = total minus cancelled
    counts = {
        'total': agg['total'],
        'open': agg['total'] - agg['cancelled'],
        'completed': agg['completed'],
        'cancelled': agg['cancelled'],
        # (optional) expose active if you want to show it anywhere
        'active': agg['active'],
    }
    return render(request, 'profile.html', {'user': user, 'quotes': quotes, 'counts': counts})



@login_required
def cancel_quote(request, pk):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    quote = get_object_or_404(Quote, pk=pk)

    # Only the requester (or staff) can cancel
    if quote.user_id != request.user.id and not request.user.is_staff:
        return HttpResponseForbidden("You cannot cancel this quote.")

    if not quote.can_cancel:
        messages.info(request, "This quote cannot be cancelled.")
        return redirect("profile")

    quote.status = Quote.STATUS_CANCELLED
    quote.save(update_fields=["status"])
    messages.success(request, "Your quote request was cancelled.")
    return redirect("profile")
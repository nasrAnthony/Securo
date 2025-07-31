from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden, HttpResponseNotAllowed
from .forms import CustomUserCreationForm, CustomUserLoginForm, QuoteForm, EditProfileForm
from django.db.models import Count, Q
from django.db import transaction
from .utils import fetch_orphan_quotes
from .models import Quote

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            fetch_orphan_quotes(user)
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
            fetch_orphan_quotes(user)
            return redirect('home')
    else:
        form = CustomUserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

OPEN_STATUS = "active"

def quote_request_view(request):
    form = QuoteForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        quote = form.save(commit=False)
        if request.user.is_authenticated:
            quote.user = request.user
            if not quote.email:
                quote.email = request.user.email
        quote.save()
        messages.success(request, "Your quote request was received. We’ll be in touch shortly.")
        return redirect('home')

    has_open = False
    open_count = 0
    if request.user.is_authenticated:
        open_count = Quote.objects.filter(user=request.user, status=OPEN_STATUS).count()
        has_open = open_count > 0

    return render(request, 'quote_form.html', {
        'form': form,
        'has_open': has_open,
        'open_count': open_count,
    })

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

@login_required
@transaction.atomic
def profile_edit(request):
    user = request.user
    old_email = user.email

    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            updated_user = form.save()  # saves email / phone_number
            new_email = updated_user.email

            # If email changed, update all quotes owned by this user (FK) to reflect the new email
            if old_email.strip().lower() != (new_email or "").strip().lower():
                Quote.objects.filter(user=updated_user).exclude(email=new_email).update(email=new_email)

                from accounts.utils import fetch_orphan_quotes
                fetch_orphan_quotes(updated_user, email=new_email)

                messages.success(request, "Your profile has been updated. We synced your quotes to the new email.")
            else:
                messages.success(request, "Your profile has been updated.")
            return redirect("profile_edit")
    else:
        form = EditProfileForm(instance=user)

    return render(request, "accounts/edit_profile.html", {"form": form})


@login_required
@transaction.atomic
def delete_account(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    user = request.user
    CANCELLED_STATUS = getattr(Quote, "STATUS_CANCELLED", "cancelled")  # or "expired"

    # 1) Cancel + orphan all quotes owned by the user (single UPDATE)
    Quote.objects.filter(user=user).update(status=CANCELLED_STATUS, user=None)

    # 2) Delete user
    user.delete()

    # 3) Log out (flush session) and redirect home
    logout(request)
    messages.success(request, "Your account has been deleted. Your quotes were cancelled.")
    return redirect("home")
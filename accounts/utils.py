from django.db import transaction
from .models import Quote

@transaction.atomic
def fetch_orphan_quotes(user, email: str | None = None) -> int:
    if not user or not(email or user.email):
        return 0
    email_norm = (email or user.email or "").strip()
    if not email_norm:
        return 0
    return Quote.objects.filter(user__isnull= True, email__iexact= email_norm).update(user=user)
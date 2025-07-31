from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from django.db import models
import uuid

# Create your models here.


#Super user class
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique= True)
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'phone_number']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    

class Quote(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL,null=True, blank=True, related_name='quotes')
    email = models.EmailField(blank=False, db_index=True)
    full_name = models.CharField(max_length=100, blank=False)
    business_name = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=15, blank=False)
    submitted_at = models.DateTimeField(auto_now_add= True)
    project_details = models.TextField()
    address = models.CharField(max_length=100)
    unit = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=100)

    PROPERTY_TYPE_CHOICES = [
        ('Commercial', 'Commercial'),
        ('Single Home', 'Single Home'),
        ('Town House', 'Town House'),
        ('Apartment', 'Apartment'),
        ('Condo', 'Condo'),
        ('Studio', 'Studio'),
    ]

    preferred_date = models.DateField(default=timezone.now)
    PREFERRED_TIME_CHOICES = [
        ('9am-12pm', '9:00 AM – 12:00 PM'),
        ('12pm-3pm', '12:00 PM – 3:00 PM'),
        ('3pm-6pm', '3:00 PM – 6:00 PM'),
    ]
    preferred_time = models.CharField(max_length=20, 
                                      choices=PREFERRED_TIME_CHOICES, 
                                        default='9am-12pm')

    property_type = models.CharField(
        max_length=20,
        choices=PROPERTY_TYPE_CHOICES,
        blank=False
    )

    STATUS_ACTIVE     = 'active'
    STATUS_COMPLETED  = 'completed'
    STATUS_EXPIRED    = 'expired'
    STATUS_CANCELLED  = 'cancelled'

    STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Active'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_EXPIRED, 'Expired'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_ACTIVE,
        db_index=True,
    )

    @property
    def can_cancel(self) -> bool:
        return self.status == self.STATUS_ACTIVE


class Invoice(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='invoices')
    invoice_number = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=[('active', 'Active'), ('paid', 'Paid'), ('canceled', 'Canceled')])
    created_at = models.DateTimeField(auto_now_add=True)
from django.contrib.auth.models import AbstractUser, BaseUserManager, Permission, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from datetime import timedelta
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _
from smart_selects.db_fields import ChainedForeignKey


# Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError("Users must have a username")
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, email, password, **extra_fields)


class OTP(models.Model):
    class PurposeChoices(models.TextChoices):
        LOGIN = 'login', 'Login'
        RESET_PASSWORD = 'reset_password', 'Reset Password'
        CHANGE_EMAIL = 'change_email', 'Change Email'
        UPDATE_PHONE = 'update_phone', 'Update Phone'
    
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name="otps")
    otp = models.CharField(max_length=255) 
    expires_at = models.DateTimeField(null=True, blank=True) 
    purpose = models.CharField(
        max_length=50,
        choices=PurposeChoices.choices,
        default=PurposeChoices.LOGIN
    ) 
    is_used = models.BooleanField(default=False) 

    def __str__(self):
        return f"OTP for {self.user.email} ({self.purpose})"

    @property
    def is_expired(self):
        """Check if the OTP has expired"""
        return timezone.now() > self.expires_at

    def check_otp(self, raw_otp):
        return not self.is_used and check_password(raw_otp, self.otp) and not self.is_expired

    def generate_otp(self, length=6, allowed_chars='23456789'):
        return get_random_string(length, allowed_chars)

    def set_otp(self, raw_otp=None, valid_for_minutes=10):
        """
        Generates and stores a hashed OTP. Sets the expiration date and time.
        """
        if raw_otp is None:
            raw_otp = self.generate_otp()  # Generate OTP if not provided
        self.otp = make_password(raw_otp)  # Store OTP hash
        self.expires_at = timezone.now() + timedelta(minutes=valid_for_minutes)
        self.is_used = False
        self.save(update_fields=['otp', 'expires_at', 'is_used'])
        return raw_otp  # Return raw OTP for delivery to user


class OtpMixin:
    """
    Mixin that provides utility methods for managing OTP functionality.
    """

    def create_otp(self, purpose=OTP.PurposeChoices.LOGIN, valid_for_minutes=10):
        """Creates and sends OTP for the given purpose."""
        otp_instance = OTP.objects.create(user=self, purpose=purpose)
        raw_otp = otp_instance.set_otp(valid_for_minutes=valid_for_minutes)  # Generate OTP and save
        return raw_otp  # Return the raw OTP for sending (email/SMS)

    def validate_otp(self, raw_otp, purpose=OTP.PurposeChoices.LOGIN):
        """Validates the OTP for a given purpose."""
        otp_instance = OTP.objects.filter(user=self, purpose=purpose, is_used=False).last()

        if otp_instance is None or not otp_instance.check_otp(raw_otp):
            raise ValidationError("Invalid or expired OTP.")
        
        # Mark OTP as used after successful validation
        otp_instance.is_used = True
        otp_instance.save()
        return True  # OTP is valid and used


# Custom User Model
class User(AbstractUser, OtpMixin, PermissionsMixin):
    email = models.EmailField(unique=True)  # Keep email as unique identifier
    username = models.CharField(max_length=150, unique=True)  # Restore username

    department = models.ForeignKey(
        "Department", on_delete=models.SET_NULL, null=True, blank=True, related_name="users"
    )

    sub_department = ChainedForeignKey(
        "Department",
        chained_field="department",
        chained_model_field="parent",
        show_all=False,
        auto_choose=True,
        sort=True,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="sub_users"
    )

    role = models.ForeignKey("Role", on_delete=models.SET_NULL, null=True, blank=True, related_name="user_set",
        related_query_name="user",)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = UserManager()

    class Meta:
        default_permissions = ()

    @classmethod
    def get_by_identifier(cls, identifier):
        """
        Retrieve a user by email, mobile, or username.
        """
        identifier_type = None
        try:
            if '@' in identifier:
                identifier_type = 'email'
                user =  cls.objects.get(email__iexact=identifier)
            elif identifier.isdigit():
                identifier_type = 'phone_number'
                user =  cls.objects.get(mobile=identifier)
            else:  # Assume it's a username
                identifier_type = 'username'
                user =  cls.objects.get(username__iexact=identifier)
            return user, identifier_type
        except cls.DoesNotExist:
            raise ValueError(_(f"User with this {identifier_type} does not exist."))

    def __str__(self):
        return self.email
 
# User Detail Table
class UserDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="details")
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.email} - Details"


class UserDocument(models.Model):
    DOCUMENT_CHOICES=[
        ('profile_image', 'Profile Image'),
        ('other', 'Other'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="documents")
    document_type = models.CharField(max_length=50, choices=DOCUMENT_CHOICES)
    document = models.FileField(upload_to='documents/')
    document_name = models.CharField(max_length=256, null=False, blank=False) 
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.document_type}"

# Role Table
class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    permissions = models.ManyToManyField(Permission, blank=True)  # Linking Django permissions

    def __str__(self):
        return self.name

# Department with Sub-Departments
class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    parent = models.ForeignKey(  # Self-referencing for sub-departments
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="sub_departments"
    )

    def __str__(self):
        return f"{self.parent.name} -> {self.name}" if self.parent else self.name


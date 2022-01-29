from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from model_utils.managers import InheritanceManager
from phonenumber_field.modelfields import PhoneNumberField

USER = settings.AUTH_USER_MODEL


class User(AbstractUser):
    """
    Default custom user model for revyz.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})


class BaseManager(InheritanceManager):
    def get_queryset(self):
        return super().get_queryset()


class BaseModel(models.Model):
    """
    Base Model. To be used for Inheriting all the fields.
    """

    created_by = models.ForeignKey(
        USER,
        verbose_name=_("Created By"),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    objects = BaseManager()

    class Meta:
        abstract = True


class City(BaseModel):
    """
    city model
    """

    city_name = models.CharField(_("City Name"), max_length=60)
    is_active = models.BooleanField(_("Is City Active?"), default=True)

    class Meta:
        verbose_name = _("City")
        verbose_name_plural = _("Cities")

    def __str__(self):
        return self.city_name


class TechnicalSkill(BaseModel):
    """
    Defines Technical skills
    """

    skill_name = models.CharField(_("Technical Skill Name"), max_length=25)
    is_active = models.BooleanField(_("Is Tech Skill Active"), default=True)

    class Meta:
        verbose_name = _("Technical skill")
        verbose_name_plural = _("Technical skills")

    def __str__(self):
        return self.skill_name


class Candidate(BaseModel):

    """
    defines candidate details models
    """

    name = models.CharField(_("Candidate Name"), max_length=60)
    email = models.EmailField(_("candidate Email"), max_length=60)
    phonenumber = PhoneNumberField()
    address = models.CharField(_("Candidate Address"), max_length=255)
    city_id = models.ForeignKey(
        City,
        verbose_name=_("City"),
        related_name="candidate_city",
        on_delete=models.CASCADE,
    )
    tech_skills = models.ManyToManyField(
        TechnicalSkill,
        verbose_name=_("TechnicalSkills"),
        related_name="candidate_skills",
    )

    class Meta:
        verbose_name = _("Candidate Details")
        verbose_name_plural = _("Candidate Details")

    def __str__(self):
        return self.skill_name

#!/usr/bin/env python
# coding=utf-8

"""OTP Admin Panel."""

from os import path
import re


from urllib.parse import urlencode

from django import forms
from django.contrib import admin
from django.urls import reverse
from .models import OTPSecrets
from .forms import AuthenticationForm
from .widgets import OTPGenWidget


class OTPGenerationForm(forms.ModelForm):
    """OTP generation form."""

    class Meta(object):
        """Metadata."""

        model = OTPSecrets
        fields = ("user", "secret", "issuer_name")
        widgets = {
            "secret": OTPGenWidget(embed_script=True, attrs={
                "class": "secret"
            })
        }

    def __init__(self, *args, **kwargs):
        """Init the instance."""
        super(OTPGenerationForm, self).__init__(*args, **kwargs)

        def fire_gen(gen_new=True):
            return (
                "var select=document.querySelector('#{0}');"
                "assignOTPSecret("
                "select.options[select.selectedIndex].text,"
                "document.querySelector('#{1}_container .secret'),"
                "document.querySelector('#{1}_container .qrcode'),"
                "'{2}', document.querySelector('#{3}').value,{4}"
                ");"
            ).format(
                self["user"].id_for_label,
                self["secret"].id_for_label,
                re.sub(r"/A{16}$", "", reverse(
                    "django_otp:qrcode",
                    kwargs={"secret": "AAAAAAAAAAAAAAAA"}
                )),
                self["issuer_name"].id_for_label,
                str(gen_new).lower()
            )
        self.fields["issuer_name"].widget.attrs["onblur"] = fire_gen(False)
        self.fields["secret"].widget.btn_attrs["onclick"] = fire_gen()
        self.fields["secret"].widget.img_attrs.setdefault("class", "")
        self.fields["secret"].widget.img_attrs["class"] += " qrcode"
        if self.instance.secret:
            self.fields["secret"].widget.img_attrs["src"] = reverse(
                "django_otp:qrcode", kwargs={"secret": self.instance.secret}
            ) + ("?{}").format(urlencode({
                key: value
                for (key, value) in {
                    "name": self.instance.user.username,
                    "issuer_name": self.instance.issuer_name
                }.items() if value
            }))


class OTPAdmin(admin.ModelAdmin):
    """OTPSecret Admin."""

    list_display = ("user", )
    search_fields = (
        "user__email", "user__first_name", "user__last_name",
        "issuer_name", "user__username"
    )
    form = OTPGenerationForm

    @classmethod
    def enable(cls):
        """Assign the model to the panel."""
        admin.site.register(OTPSecrets, cls)


class AdminSite(admin.AdminSite):
    """AdminSite."""

    login_form = AuthenticationForm
    login_template = path.join(
        path.abspath(path.dirname(__file__)),
        "templates", "login.html",
    )

    def __init__(self, *args, **kwargs):
        """Initialize the instance."""
        inherit = bool(kwargs.pop("inherit_panels", True))
        super(AdminSite, self).__init__(*args, **kwargs)
        if inherit:
            self._registry.update(admin.site._registry)

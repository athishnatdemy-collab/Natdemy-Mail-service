# from django.http import JsonResponse
# from .cpanel import create_email
# def create_employee_email(request):

#     email = request.POST.get("email")
#     password = request.POST.get("password")

#     result = create_email(email, password)

#     return JsonResponse(result)


import logging
import requests

from django.conf import settings
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

logger = logging.getLogger(__name__)

# cPanel credentials should be defined in settings or environment variables.
# Example settings.py entries:
#   CPANEL_USER = "real_user"
#   CPANEL_TOKEN = "real_token"
#   CPANEL_URL = "https://yourdomain.com:2083"
CPANEL_USER = getattr(settings, "CPANEL_USER", "")
CPANEL_TOKEN = getattr(settings, "CPANEL_TOKEN", "")
CPANEL_URL = getattr(settings, "CPANEL_URL", "")
ADMIN_PASSWORD = getattr(settings, "ADMIN_PASSWORD", "")


@require_http_methods(["GET", "POST"])
def create_email(request):
    """Render the form and call cPanel API to create a mailbox."""

    message = ""

    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        employee_name = request.POST.get("name", "").strip()
        password = request.POST.get("password", "")
        quota = request.POST.get("quota", "500")
        admin_password = request.POST.get("admin_password", "")

        if not admin_password or admin_password != ADMIN_PASSWORD:
            message = "Invalid admin password. Email creation denied."
        elif not email or not password:
            message = "Email username and password are required."
        elif not CPANEL_USER or not CPANEL_TOKEN or not CPANEL_URL:
            message = "Server configuration is incomplete. Contact administrator."
        else:
            url = f"{CPANEL_URL}/execute/Email/add_pop"
            headers = {"Authorization": f"cpanel {CPANEL_USER}:{CPANEL_TOKEN}"}
            payload = {
                "email": email,
                "domain": "natdemy.in",
                "password": password,
                "quota": quota,
            }

            try:
                response = requests.post(url, headers=headers, data=payload, timeout=10)
            except requests.RequestException as exc:
                logger.exception("cPanel request failed")
                message = "Network error while creating email."
            else:
                if response.status_code == 200:
                    message = f"Email {email}@natdemy.in created successfully"
                else:
                    logger.error(
                        "cPanel API error %s: %s", response.status_code, response.text
                    )
                    message = (
                        "Error creating email: "
                        f"{response.status_code} - {response.text[:200]}"
                    )

    return render(request, "create_email.html", {"message": message})
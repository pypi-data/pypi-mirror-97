import requests
import importlib
from urllib.parse import unquote

from rest_framework.exceptions import PermissionDenied
from django.conf import settings


__all__ = (
    'CredentialMixin',
    'SmartAdminRequiredMixin',
)


class BaseCredentialMixin(object):

    if settings.DASHBOARD_URL.endswith("/"):
        url = settings.DASHBOARD_URL
    else:
        url = settings.DASHBOARD_URL + '/'

    def get_user_info(self, request):
        if 'token' in request.GET and "platform_id" in request.GET:
            token = unquote(request.GET["token"])
        elif 'HTTP_AUTHORIZATION' in request.META and "platform_id" in request.GET:
            token = request.META["HTTP_AUTHORIZATION"]
        else:
            raise PermissionDenied(
                {"status": "error", "message": "you don't have permission to access"}
            )
        try:
            response = requests.get(
                f"{self.url}api/check-platform/?platform_id={request.GET['platform_id']}",
                headers={"executetoken": token},
            )
        except requests.ConnectionError:
            raise PermissionDenied(
                {"status": "error", "message": "Authorization failed."}
            )

        if response.status_code != 200:
            raise PermissionDenied(
                {"status": "error", "message": "Authorization failed."}
            )

        return response.json()["auth_info"]

    def get_check_admin(self, request, *args, **kwargs):
        user_info = self.get_user_info(request, *args, **kwargs)
        user_id = user_info["id"]
        if user_id in (19, 22, 23, 55):
            return user_id
        raise PermissionDenied(
            {"status": "error", "message": "This endpoint only for smart admin users."}
        )


class CredentialMixin(BaseCredentialMixin):

    check_credential = True
    with_smart_auth = True

    # method for dashboard app
    def get_check_dash_auth(self, request):
        if 'HTTP_EXECUTETOKEN' not in request.META:
            raise PermissionDenied(
                {"status": "error", "message": "you don't have permission to access"}
            )
        auth_info = requests.post(
            f"{self.url}api/check-auth/",
            headers={"executetoken": request.META['HTTP_EXECUTETOKEN']},
        ).json()
        if "is_admin" not in auth_info:
            raise PermissionDenied({"status": "error", "message": "Invalid dash user."})

        return auth_info["is_admin"]

    def check_mongo_credential(self):
        mongo_credential = getattr(settings, 'MONGODANTIC_CREDENTIAL', False)
        return mongo_credential

    def get_credential(self, request, model=None, mongodantic=False):
        """[summary]

        Arguments:
            request {HttpRequest} -- django http request

        Keyword Arguments:
            model {django model or None} -- django model (default: {None})

        Raises:
            PermissionDenied: if not credential exists

        Returns:
            django model -- credential object
        """
        if not model:
            model = self.get_credential_model()

        cred_id = request.GET.get("credential_id")
        mongodantic = mongodantic or self.check_mongo_credential()
        if not mongodantic:
            params = {
                'id': cred_id,
            }

            credential = model.objects.filter(**params).first()
        else:
            params = {
                '_id': cred_id,
            }

            credential = model.querybuilder.find_one(**params)
        if not credential:
            raise PermissionDenied(
                {"status": "error", "message": "Credential does not exist."}
            )

        return credential

    def initial(self, request, *args, **kwargs):
        if self.with_smart_auth:
            user_info = self.get_user_info(request)
            self.smart_user_id = user_info['id']
            self.smart_username = user_info['username']
            if hasattr(settings, 'CREDENTIAL_MODEL') and self.check_credential:
                self.credential = self.get_credential(request)
        return super().initial(request, *args, **kwargs)

    def get_credential_model(self):
        if hasattr(settings, 'CREDENTIAL_MODEL'):
            module_path, model = settings.CREDENTIAL_MODEL.rsplit('.', 1)
            module = importlib.import_module(module_path)
            return getattr(module, model)
        raise AttributeError('miss CREDENTIAL_MODEL in django settings')


class SmartAdminRequiredMixin(BaseCredentialMixin):
    def initial(self, request, *args, **kwargs):
        self.get_check_admin(request)
        return super().initial(request, *args, **kwargs)

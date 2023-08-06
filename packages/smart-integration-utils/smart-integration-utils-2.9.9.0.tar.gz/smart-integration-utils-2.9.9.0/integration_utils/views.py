from typing import Optional
from django.http import HttpResponseRedirect
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView

from .exceptions import InvalidDateParams, InvalidFieldsParam
from .mixins import CredentialMixin
from .pagination import LimitOffsetPaginationListAPIView

__all__ = (
    'HomeAPIView',
    'BaseCredentialModelViewSet',
    'BaseReportListAPIView',
    'BaseGetCredentialAPIView',
    'BaseStatTSVAPIView',
)


class BaseCredentialModelViewSet(CredentialMixin, ModelViewSet):
    check_credential = False
    queryset = None
    serializer_class = None

    def get_queryset(self):
        if not self.queryset:
            raise NotImplementedError("model must be declare")
        return self.queryset

    def create(self, request, format=None):
        raise NotImplementedError()

    def retrieve(self, request, *args, **kwargs):
        """
        ---
        parameters:
            - Authorization token in headers
        """

        _ = self.get_check_dash_auth(request)
        return super().retrieve(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """
        ---
        parameters:
            - Authorization token in headers
        """
        _ = self.get_check_dash_auth(request)

        return super().list(request, *args, **kwargs)


# base View model
class BaseReportListAPIView(LimitOffsetPaginationListAPIView):
    serializer_class = None
    model = None
    select_related_fields = ()  # must be tuple or list
    with_platforms_sample = False
    order_by_fields = ()  # must be tuple or list
    filter_params = {}  # custom filter params

    def get_model(self):
        if not self.model:
            raise NotImplementedError("model must be declare")
        return self.model

    def get_queryset(self):
        if self.select_related_fields and isinstance(
            self.select_related_fields, (tuple, list)
        ):
            qs = (
                self.get_model()
                .objects.select_related(*self.select_related_fields)
                .filter(
                    integration_id=self.integration_id,
                    date__range=[self.date_from, self.date_to],
                    **self.filter_params,
                )
            )
        else:
            qs = self.get_model().objects.filter(
                integration_id=self.integration_id,
                date__range=[self.date_from, self.date_to],
                **self.filter_params,
            )
        if self.with_platforms_sample:
            return qs.filter(platform_id=self.platform_id)
        if self.order_by_fields:
            return qs.order_by(*self.order_by_fields)
        return qs


class BaseGetCredentialAPIView(CredentialMixin, APIView):
    def get_redirect_uri(self):
        """Create in this method redirect uri
            Example: https://oauth.yandex.ru/authorize?response_type=code&client_id={settings.YANDEX_APP_CLIENT_ID}&state={self.get_state()}&redirect_uri={redirect_url}
        """
        raise NotImplementedError()

    def check_auth_params(self):
        """This method for check auth params"""
        if (
            "callback_url" not in self.request.GET
            or "token" not in self.request.GET
            or "platform_id" not in self.request.GET
        ):
            raise PermissionDenied(
                {"status": "error", "message": "You dont have permission to access."}
            )
        return self.request

    def get_state(self):
        """
            Create state in this method
            Excample:
                user_info = self.get_user_info(request, get_token=True)
                user_id = user_info["id"]
                main_user = user_info["username"]
                # user_id = 16
                # main_user = "main_user"

                state = {
                    "callback_url": request.GET['callback_url'],
                    "user_id": user_id,
                    "main_user": main_user,
                    "platform_id": request.GET['platform_id']
                }
                return state
        """
        raise NotImplemented()

    def get(self, request, format=None):
        """
        ---
        parameters:
            - Authorization token in headers
            - 'callback_url' in GET params
        """

        return HttpResponseRedirect(self.get_redirect_uri())


class HomeAPIView(CredentialMixin, APIView):
    def get(self, request, format=None):
        return Response({"status": "success", "message": "smart integration api"})


class BaseStatTSVAPIView(CredentialMixin, APIView):
    check_credential = False
    serializer_class = None

    def get_serializer_class(self):
        if not self.serializer_class:
            raise NotImplementedError('serializer_class must be implemented!')
        return self.serializer_class

    def check_log(self, *args, **kwargs) -> None:
        """check any download log,

        Returns:
            None: or raise APIException
        """
        return None

    def validate_request_data(self, request) -> dict:
        admin = self.get_check_admin(request)
        # return Response({"status": "error", "message": "Dont have statistic for this integration"}, status=400)
        if not admin:
            raise PermissionDenied(
                {
                    "status": "error",
                    "message": "You don't have permissions for this endpoint.",
                }
            )
        data = request.data
        integration_id = data.get("integration_id")

        if not integration_id:
            return (
                InvalidDateParams(
                    {"status": "error", "message": "Miss integration id."}, status=422
                ),
            )

        values = list()
        if 'fields' in data:
            serializer = self.get_serializer_class()
            fields = list(serializer().fields.keys())
            for f in data['fields']:
                if f in fields:
                    values.append(f)
                else:
                    raise InvalidFieldsParam(
                        {"status": "error", "message": f"invalid field - {f}"}
                    )
        self.check_log()
        return {
            'data': data,
            'integration_id': integration_id,
            'admin': admin,
            'platform_id': request.GET['platform_id'],
            'values': values,
        }


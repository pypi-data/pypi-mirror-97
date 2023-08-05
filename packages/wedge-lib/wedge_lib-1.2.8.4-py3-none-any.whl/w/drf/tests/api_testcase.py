import json

from django.conf import settings

from rest_framework import status as drf_status
from rest_framework.test import APIClient

from rest_framework_api_key.models import APIKey
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token

from w import Debug
from w.django.tests.django_testcase import DjangoTestCase
from w.django.tests.factories.auth_factories import UserFactory
from w.django.utils import reverse


class ApiTestCase(DjangoTestCase):
    """ Class to handle common API test functionalities """

    show_json_response = False
    default_user = None
    default_token = None
    default_api_key = None
    client_class = APIClient

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.factory_boy_seed_random()

    def _get_user(self):
        if self.default_user is None:
            self.default_user = UserFactory(
                username="factory-boy",
                first_name="Factory",
                last_name="Boy",
                email="fb@factory.com",
            )
        return self.default_user

    def force_authenticate(self, user=None):
        """
        Force authenticate, if no user given, use a default one
        (created via factory_boy)

        Args:
            user (User): user to authenticate (optional)
        """
        if user is None:
            user = self._get_user()
        self.client.force_authenticate(user=user)

    @staticmethod
    def _get_jwt_access_token(user):
        jwt_token = RefreshToken.for_user(user)
        return str(jwt_token.access_token)

    @staticmethod
    def _get_token(user):
        if hasattr(settings, "SIMPLE_JWT"):
            jwt_token = RefreshToken.for_user(user)
            return str(jwt_token.access_token)
        token, created = Token.objects.get_or_create(user=user)
        return token

    def _get_token_header(self, user):
        header_token_keyword = "Bearer" if hasattr(settings, "SIMPLE_JWT") else "Token"
        if user:
            token = self._get_token(user)
            return f"{header_token_keyword} {token}"

        if self.default_token is None:
            self.default_token = self._get_token(self._get_user())

        return f"{header_token_keyword} {self.default_token}"

    def _add_api_key_header(self, params):
        API_KEY_CUSTOM_HEADER = (
            settings.API_KEY_CUSTOM_HEADER
            if hasattr(settings, "API_KEY_CUSTOM_HEADER")
            else None
        )
        if self.default_api_key is None:
            _, self.default_api_key = APIKey.objects.create_key(
                name="my-remote-service"
            )
        params[API_KEY_CUSTOM_HEADER] = self.default_api_key

    def set_client_params(self, params, auth_by_token=True, user=None):
        if auth_by_token:
            params["HTTP_AUTHORIZATION"] = self._get_token_header(user)

        self._add_api_key_header(params)

    def _client_method(self, method, url, data=None, auth_by_token=True, user=None):
        params = {"path": url, "data": data}
        self.set_client_params(params, auth_by_token, user)
        return getattr(self.client, method)(**params)

    def client_get(self, url, auth_by_token=True, user=None):
        return self._client_method("get", url, auth_by_token=auth_by_token, user=user)

    def client_post(self, url, data=None, auth_by_token=True, user=None):
        return self._client_method(
            "post", url, data=data, auth_by_token=auth_by_token, user=user
        )

    def client_put(self, url, data=None, auth_by_token=True, user=None):
        return self._client_method(
            "put", url, data=data, auth_by_token=auth_by_token, user=user
        )

    def client_delete(self, url, data=None, auth_by_token=True, user=None):
        return self._client_method(
            "delete", url, data=data, auth_by_token=auth_by_token, user=user
        )

    def client_patch(self, url, data=None, auth_by_token=True, user=None):
        return self._client_method(
            "patch", url, data=data, auth_by_token=auth_by_token, user=user
        )

    def _assert_no_registered_user_return_401(self, method, urlconf, url_params):
        response = getattr(self.client, method)(reverse(urlconf, kwargs=url_params))
        self.assert_rest_status_code(response, drf_status.HTTP_401_UNAUTHORIZED)

    def _assert_unauthorized_user_return_403(
        self, method, url_name, url_params, user=None, data=None
    ):
        params = {"url": reverse(url_name, kwargs=url_params), "user": user}
        if data is not None:
            params["data"] = data
        response = getattr(self, f"client_{method}")(**params)
        self.assert_rest_status_code(response, drf_status.HTTP_403_FORBIDDEN)

    def _assert_unknown_resource_return_404(self, method, urlconf, url_params):
        response = getattr(self, f"client_{method}")(
            reverse(urlconf, kwargs=url_params)
        )
        self.assert_rest_status_code(response, drf_status.HTTP_404_NOT_FOUND)

    def assert_get_with_no_registered_user_return_401(self, urlconf, url_params=None):
        """ Ensure we cannot get if no user authenticated """
        self._assert_no_registered_user_return_401("get", urlconf, url_params)

    def assert_get_with_unauthorized_user_return_403(
        self, user, urlconf, url_params=None
    ):
        """ Ensure we cannot get if user is not authorized """
        self._assert_unauthorized_user_return_403("get", user, urlconf, url_params)

    def assert_get_with_unknown_resource_return_404(self, urlconf, url_params=None):
        """ Ensure we cannot get if resource is unknown """
        self._assert_unknown_resource_return_404("get", urlconf, url_params)

    def assert_post_with_no_registered_user_return_401(self, urlconf, url_params=None):
        """ Ensure we cannot post if no user authenticated """
        self._assert_no_registered_user_return_401("post", urlconf, url_params)

    def assert_post_with_unauthorized_user_return_403(
        self, urlconf, url_params=None, user=None, data=None
    ):
        """ Ensure we cannot post if user is not authorized """
        self._assert_unauthorized_user_return_403(
            "post", urlconf, url_params=url_params, user=user, data=data
        )

    def assert_post_with_unknown_resource_return_404(self, urlconf, url_params=None):
        """ Ensure we cannot post if resource is unknown """
        self._assert_unknown_resource_return_404("post", urlconf, url_params)

    def assert_put_with_no_registered_user_return_401(self, urlconf, url_params=None):
        """ Ensure we cannot put if no user authenticated """
        self._assert_no_registered_user_return_401("put", urlconf, url_params)

    def assert_put_with_unauthorized_user_return_403(
        self, urlconf, url_params=None, user=None, data=None
    ):
        """ Ensure we cannot put if user is not authorized """
        self._assert_unauthorized_user_return_403(
            "put", urlconf, url_params=url_params, user=user, data=data
        )

    def assert_put_with_unknown_resource_return_404(self, urlconf, url_params=None):
        """ Ensure we cannot put if resource is unknown """
        self._assert_unknown_resource_return_404("put", urlconf, url_params)

    def assert_patch_with_no_registered_user_return_401(self, urlconf, url_params=None):
        """ Ensure we cannot patch if no user authenticated """
        self._assert_no_registered_user_return_401("patch", urlconf, url_params)

    def assert_patch_with_unauthorized_user_return_403(
        self, urlconf, url_params=None, user=None, data=None
    ):
        """ Ensure we cannot patch if user is not authorized """
        self._assert_unauthorized_user_return_403(
            "patch", urlconf, url_params=url_params, user=user, data=data
        )

    def assert_patch_with_unknown_resource_return_404(self, urlconf, url_params=None):
        """ Ensure we cannot patch if resource is unknown """
        self._assert_unknown_resource_return_404("patch", urlconf, url_params)

    def assert_delete_with_no_registered_user_return_401(
        self, urlconf, url_params=None
    ):
        """ Ensure we cannot delete if no user authenticated """
        self._assert_no_registered_user_return_401("delete", urlconf, url_params)

    def assert_delete_with_unauthorized_user_return_403(
        self, urlconf, url_params=None, user=None, data=None
    ):
        """ Ensure we cannot delete if user is not authorized """
        self._assert_unauthorized_user_return_403(
            "delete", urlconf, url_params=url_params, user=user, data=data
        )

    def assert_delete_with_unknown_resource_return_404(self, urlconf, url_params=None):
        """ Ensure we cannot delete if resource is unknown """
        self._assert_unknown_resource_return_404("delete", urlconf, url_params)

    def assert_get_response(self, response):
        self.assert_rest_response(response, status=drf_status.HTTP_200_OK)

    def assert_post_response(self, response):
        self.assert_rest_response(response, status=drf_status.HTTP_201_CREATED)

    def assert_put_response(self, response):
        self.assert_rest_response(response, status=drf_status.HTTP_200_OK)

    def assert_patch_response(self, response):
        self.assert_rest_response(response, status=drf_status.HTTP_200_OK)

    def assert_delete_response(self, response):
        self.assert_rest_status_code(response, status=drf_status.HTTP_204_NO_CONTENT)

    @staticmethod
    def assert_rest_status_code(response, status, post_err_msg=""):
        try:
            assert status == response.status_code, (
                f"expected status {status} == {response.status_code} "
                f"actual{post_err_msg}"
            )
        except Exception as e:
            Debug.s(json.loads(response.content))
            raise e

    def assert_rest_response(self, response, status):
        self.assert_rest_status_code(response, status)
        if self.show_json_response:
            Debug.s(response.content)
        self.assert_equals_resultset(json.loads(response.content))

    def assert_invalid_data_response(self, response):
        self.assert_rest_response(
            response, status=drf_status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    @classmethod
    def save_as_cypress_fixtures(cls, fixture_path, dataset):
        """ Save dataset into cypress fixture repo """
        if settings.CYPRESS_FIXTURE_DIR is None:
            # ignore cypress fixture saving
            return None

        fixture_filename = f"{settings.CYPRESS_FIXTURE_DIR}/{fixture_path}"
        cls._save_as_fixture(fixture_filename, dataset)

    @classmethod
    def save_response_as_cypress_fixtures(cls, fixture_path, response):
        """ Save response content into cypress fixture repo """
        return cls.save_as_cypress_fixtures(fixture_path, json.loads(response.content))

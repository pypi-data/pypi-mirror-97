# utils for integrations

## install

Install using `pip`...

    pip install smart-integration-utils

# settings

```python

#add to settings.py
DASHBOARD_URL = "https://9tnvnh6ri0.execute-api.eu-central-1.amazonaws.com/dashboard/"
BUCKET_NAME = 'zappa-fullbucket'
EXECUTE_TOKEN = '<token for dashboard app>'
```

## usage

```python
# fields
from integration_utils.fields import UTF8JSONField
from django.db import models

class Entity(models.Model):
    ...
    config = UTF8JSONField() # postresql jsonb field for correct ascii characters


# mixins
#in settings.py
CREDENTIAL_MODEL = 'api.models.Credential' # or path to your credential model

from integration_utils.mixins import CredentialMixin
from rest_framework.views import APIView

class Test(CredentialMixin, APIView):
    """Now u always have self.smart_user_id and self.smart_username variables for check smart users"""
    check_credential = True or False # True for check credential in any http request, if True u can use self.credential variable.
    with_smart_auth = True or False # True for check smart user in any http request, if True u can use self.smart_user_id, self.smart_username variable.
    def get(self, request):
        ...


# serializers
from integration_utils.serialziers import GeneratorSerializer, CalculationDynamicFieldSerializer
# GeneratorSerializer instance of https://github.com/bzdvdn/drf-dynamicfieldserializer

class DataSerializer(GeneratorSerialzier):
    ...
fields = ['id', 'name']
d = DataSerilizer(queryset, response_fields=fields)
d.generator # return a generator of your data
d.data # return list of your data

class CalcDataSerializer(CalculationDynamicFieldSerializer): # for calculation data if integration have calculation step
    ...

d = DataSerilizer(queryset, response_fields=fields, context={'calculation': '<smart calc string>'})

# views
from integration_utils.veiws import BaseCredentialModelViewSet, BaseReportListAPIView, BaseStatTSVAPIView
from .models import Credential
from .serializers import CredentialSerializer

class CredentialViewSet(BaseCredentialModelViewSet): # mro CredentialMixin, ModelViewSet
    queryset = Credential.obejcts.all()
    serializer_class = CredentialSerializer


class EntityListAPIView(BaseReportListAPIView):
    """return from GET qury a paginated result from your data by integration_id and date params (date_from=2020-01-20
        &date_to=2020-01-20)"""
    model = Entity
    serializer_class = EntitySerializer
    select_related_fields = ('contact', 'manager') # if needed select_related
    with_platforms_sample = True # for queries by platform_id fields
    order_by_fields = ('-id',) # for ordering default = ()


class DataTSVAPIView(BaseStatTSVAPIView):
    serializer_class = EntitySerializer

    def post(self, request):
        data = self.validate_request_data(request)
        stats_selector = MySelector(**data)
        return stats_selector.response()

# tools
from integration_utils.tools import chunk_of_generators

list_ = [i for i in range(1, 100000000)]
chunk_of_generators(iter(list_), 25000) # split your iterator/generator for 25000 items

from integration_utils.tools import delete_file

delete_file('<path to file>') # delete file from your disc

from integration_utils.tools import write_file

data = [{str(i): i} for i in range(1, 100000000)]
 # write tsv/csv file
write_file(filename='<path_to_file>', date=data, fieldsnames = None, delimiter='\t', extension='.tsv')


from integration_utils.tools import upload_to_s3

upload_to_s3(filename='<path_to_local_file>', folder='stats/') # filename - local file, folder - folder on s3 bucket

from integration_utils.tools import get_file_link

get_file_link(filename='filename', folder='stats/', suffix='.tsv') # get link to download file(not download from boto3)

from integration_utils.tools import chunk_by_items

data = [i for i in range(1, 100000000)]
chunk_by_items(data, 10000) # return generator for split your list by 10000


from integration_utils.tools import get_full_integrations

# return all integrations from comagic integration
integrations = get_full_integrations(platform='prod', sevice_code='comagic')


from copy import copy
from integration_utils.tools import check_entities_equal
from .models import Deal
db_deal = Deal.objects.first()
new_deal = copy(db_deal)
new_deal.name = '123'

check_entities_equal(db_deal=db_deal, new_deal=new_deal) # return True/False check to deals equals


from integration_utils.tools import chunk_by_parts

data = [i for i in range(1, 100000000)]
chunk_by_parts(data, 5) # return generator for split your list by 5 pars


from integration_uils.tools import delete_s3_file

delete_s3_file(filename='filename', folder='stats/', suffix='.tsv') # delete file from s3 bucket

from integration_utils.tools import encode, decode

credential_secure_password = '1qazxsw2'
encoded = encode(credential_secure_password) # encrypt secure data
decoded = decode(encoded) # decrypt secure data

# utils
from integration_utils.utils import parse_utm

url = 'https://test.io/?utm_source=google&utm_medium=cpc&utm_campaign=1'
utm = parse_utm(url) # return {'utm_source': 'google', 'utm_medium': 'cpc', 'utm_campaign': '1'}


# filters
from integration_utils.filters import validate_data

filter_str = "url=@test.ru;!url=@google;!url=@yandex;!url=@yahoo"

## for filter you must be compare validate_obj(dict)
## check filter
validated_obj = {'url': 'test.ru/123', 'entity_id':1, 'entity_name': 'test_obj'}
validate_data(filter_str, validated_obj)

# parse for orms
from integration_utils.filters import parse_for_django_query, parse_for_mongo_query
filter_str = "url=@test.ru,!url=@google"
parse_for_django_query(filter_str) # return [{'filter': {'url__iexact': 'test.ru'}, 'exclude': {}}, {'filter': {}, 'exclude': {'url__iexact': 'google'}}]
parse_for_mongo_query(filter_str) # return [{'url__regex': 'test.ru'}, {'url__regex_ne': 'google'}]

# decode data
from integration_utils.tools import decrypt_data

# your view
data = request.data
salt = 'secure salt'
decrypted_data = decrypt_data(data, '<access_token>', salt)


```

# #changelog

- 2.9.9.0 - add BaseDataManager to services.py
- 2.9.8.6 - add more check in folder s3 functions param
- 2.9.8.5 - add exceptions.py, services.py, BaseStatsTSVAPIView
- 2.9.8.4 - add support mongodantic credential
- 2.9.8.3 - add filter_params to BaseReportListAPIView
- 2.9.8.2 - fix order_by for BaseReportListAPIView
- 2.9.8.1 - refactoring dates_delta generation
- 2.9.8 - add dates_chunker, fix fields for django 3.1
- 2.9.7 - remove InvalidJSONInput from dependencies
- 2.9.6 - fix filters
- 2.9.5 - fix parse data params in decrypt
- 2.9.4 - add decrypt_data
- 2.9.3 - add order_by_fields param to BaseReportListAPIView
- 2.9.2 - add with_smart_auth param to CredentialMixin(For dash methods)
- 2.9.1 - fix bug in credential attr
- 2.9.0 - rework CredentialMixin, now get_user_info execute with any http method, check_credential=True for check credential in db, now u need add CREDENTIAL_MODEL variable in django settings for CredentialMixin, add SmartAdminRequiredMixin.
- 2.8.9.3 - fix limit params in LimitOffsetPaginationListAPIView
- 2.8.9.2 - remove eventmonitoring-client from requirement dependencies
- 2.8.9.1 - check_user param in CredentialMixin set default to False
- 2.8.9 - fix parse_for_django_query with AND statement
- 2.8.8 - fix parse_for_mongo_query with OR statement
- 2.8.7 - upload_to_s3_from_ram now upload from BytesIO and StringIO
- 2.8.6 - support platform_id in BaseReportListAPIView
- 2.8.5 - add parse_for_mongo_query, parse_for_django_query tools in filters.py
- 2.8.4 - fix tools for python3.7
- 2.8.1 - remove parse_filters, create_filter_results from filters.py, add validate_data func

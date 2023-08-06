import json
import os
import csv
import boto3
import requests
import hashlib
from datetime import datetime, timedelta
from io import StringIO, BytesIO
from boto3.s3.transfer import TransferConfig
from Crypto.Cipher import AES
from base64 import b64encode, b64decode
from typing import Union, Optional, List, Iterator, Generator

from django.conf import settings

BUCKET_NAME = settings.BUCKET_NAME
if settings.DASHBOARD_URL.endswith("/"):
    DASHBOARD_URL = settings.DASHBOARD_URL
else:
    DASHBOARD_URL = settings.DASHBOARD_URL + "/"

__all__ = (
    'chunk_of_generators',
    'get_smart_token',
    'delete_file',
    'write_file',
    'upload_to_s3',
    'check_file_exist',
    'get_file_link',
    'chunk_by_items',
    'delete_s3_file',
    'chunk_by_parts',
    'decode',
    'encode',
    'get_full_integrations',
    'write_ram_file',
    'upload_to_s3_from_ram',
    'delete_invalid_integrations',
)


def chunk_of_generators(iterable: Union[Generator, Iterator], max_value: int = 10):
    def inner(iterator: Union[Generator, Iterator], max_value: int, switcher: list):
        switcher[0] = False
        for i in range(max_value):
            try:
                yield next(iterator)
            except StopIteration:
                return
        switcher[0] = True
        return

    iterator = iter(iterable)
    switcher = [True]
    while switcher[0] == True:
        try:
            yield inner(iterator, max_value, switcher)
        except StopIteration:
            return None


def get_smart_token(platform: str) -> str:
    """
    :param platform: str (prod or dev)
    :return: str
    """
    url = f'{DASHBOARD_URL}api/smart_tokens/?platform_id={platform}'
    token = settings.EXECUTE_TOKEN
    try:
        r = requests.get(url, headers={"executetoken": token}).json()
    except (requests.ConnectionError, json.JSONDecodeError):
        return 'error'
    return r['token']


def delete_file(filename: str):
    os.remove(filename)


def write_file(
    filename: str,
    data: Union[list, dict, Generator],
    fieldnames: Optional[List[str]] = None,
    delimiter: str = '\t',
    extension: str = '.tsv',
) -> str:
    """
    :param filename: str (path to local file)
    :param data: any (serialized data)
    :param delimiter: str
    :param extension: str
    :param fieldnames: list or None (list of fieldsnames)
    :return: bool
    """
    if extension not in filename:
        filename = f"{filename}{extension}"
    with open(filename, 'w') as f:
        if not fieldnames:
            fieldnames = list(data[0].keys())
        writer = csv.DictWriter(f, delimiter=delimiter, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)
    return filename


def upload_to_s3(filename: str, folder: str = "stats/") -> dict:
    """
    :param filename: str (path to local file)
    :param folder: str (folder from s3)
    :return: dict
    """
    s3 = boto3.resource('s3')
    GB = 1024 ** 3
    config = TransferConfig(multipart_threshold=int(GB / 3))
    if filename.startswith('/tmp/'):
        s3_filename = filename[5:]
    else:
        s3_filename = filename
    if folder.startswith('/'):
        folder = folder[1:]
    if not folder.endswith('/'):
        folder = f'{folder}/'
    s3.meta.client.upload_file(
        filename,
        BUCKET_NAME,
        f"{folder}{s3_filename}",
        ExtraArgs={'ACL': 'public-read'},
        Config=config,
    )

    return {"status": "success", "s3_filename": s3_filename, "s3_folder": folder}


def check_file_exist(filename: str, folder: str = "stats/") -> bool:
    """
    :param filename: str
    :param folder: str
    :return: bool
    """
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(BUCKET_NAME)
    if filename.startswith('/tmp/'):
        filename = filename[5:]
    if folder.startswith('/'):
        folder = folder[1:]
    if not folder.endswith('/'):
        folder = f'{folder}/'
    key = folder + filename
    objs = list(bucket.objects.filter(Prefix=key))
    if len(objs) > 0 and objs[0].key == key:
        return True
    else:
        return False


def get_file_link(
    filename: str,
    folder: str = 'stats/',
    bucket: str = BUCKET_NAME,
    suffix: str = '.tsv',
) -> str:
    """
    :param filename: str
    :param folder: str
    :param bucket:  str
    :param suffix: str
    :return: str
    """
    client = boto3.client('s3')
    if folder.startswith('/'):
        folder = folder[1:]
    if not folder.endswith('/'):
        folder = f'{folder}/'
    if filename.startswith('/tmp/'):
        filename = filename[5:]
    if suffix in filename:
        filename = f"{folder}{filename}" if folder not in filename else filename
    else:
        filename = (
            f"{folder}{filename}{suffix}"
            if folder not in filename
            else f"{filename}{suffix}"
        )
    # content = client.head_object(Bucket=BUCKET_NAME, Key=filename)
    bucket_location = client.get_bucket_location(Bucket=bucket)
    filepath = f"https://s3-{bucket_location['LocationConstraint']}.amazonaws.com/{BUCKET_NAME}/{filename}"

    return filepath


def chunk_by_items(items: list, step: int):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(items), step):
        yield items[i : i + step]


def get_full_integrations(platform: str, service_code: str) -> list:
    """
    :param platform: str (prod or dev)
    :param service_code: str (code from integration config)
    :return: list (list of integrations)
    """
    token = get_smart_token(platform)
    url = f'{DASHBOARD_URL}api/get_config_url/'
    dash_response = requests.get(f'{url}?platform_id={platform}').json()
    headers = {"Authorization": token}

    config_url = f'{dash_response["config_url"]}?type__code={service_code}&all=1'
    # print(config_url)

    configs = requests.get(config_url, headers=headers).json()
    results = configs["results"]
    while configs["next"]:
        configs = requests.get(configs["next"], headers=headers).json()
        results.extend(configs["results"])
    return results


def check_entities_equal(
    db_entity: any, new_entity: any, exclude_fields: Union[list, tuple, None] = None
) -> bool:
    """
    :param db_entity: any
    :param new_entity: any
    :return: bool
    """
    db_entity = db_entity.__dict__
    new_entity = new_entity.__dict__
    if not exclude_fields:
        exclude_fields = (
            '_state',
            'date_time',
            'sc_date_time',
            'funnel_stage_duration',
            'id',
        )
    return all(
        (field, new_entity[field]) in db_entity.items()
        for field in db_entity
        if field not in exclude_fields
    )


def chunk_by_parts(seq: list, parts: int) -> list:
    """
    :param seq: list
    :param parts: int
    :return: list
    """
    if len(seq) < parts:
        return [seq]
    avg = len(seq) / float(parts)
    out = []
    last = 0.0
    while last < len(seq):
        out.append(seq[int(last) : int(last + avg)])
        last += avg
    return out


def delete_s3_file(filename: str, folder: str, suffix: str) -> str:
    """
    :param filename: str (like /tmp/yandex_stats)
    :param folder: str (s3 folder name like stats/)
    :param suffix: str (end of file like .csv)
    :return: str
    """
    if filename.startswith('/tmp/'):
        filename = filename[5:]
    client = boto3.client('s3')
    if suffix not in filename:
        filename = f"{filename}{suffix}"
    if folder.startswith('/'):
        folder = folder[1:]
    if not folder.endswith('/'):
        folder = f'{folder}/'
    if folder not in filename:
        filename = f"{folder}{filename}"
    client.delete_object(Bucket=BUCKET_NAME, Key=filename)
    return f"{filename} - deleted!"


class __Crypt(object):
    def __init__(self, salt='SlTKeYOpHygTYkP3'):
        self.salt = salt
        self.enc_dec_method = 'utf-8'

    def encrypt(self, str_to_enc, str_key=settings.SECRET_KEY):
        try:
            aes_obj = AES.new(
                hashlib.sha256(str_key.encode()).digest(), AES.MODE_CFB, self.salt
            )
            hx_enc = aes_obj.encrypt(str_to_enc)
            mret = b64encode(hx_enc).decode(self.enc_dec_method)
            mret = mret.replace('/', '-_-')
            return mret
        except ValueError as value_error:
            if value_error.args[0] == 'IV must be 16 bytes long':
                raise ValueError('Encryption Error: SALT must be 16 characters long')
            elif (
                value_error.args[0] == 'AES key must be either 16, 24, or 32 bytes long'
            ):
                raise ValueError(
                    'Encryption Error: Encryption key must be either 16, 24, or 32 characters long'
                )
            else:
                raise ValueError(value_error)

    def decrypt(self, enc_str, str_key=settings.SECRET_KEY):
        try:
            enc_str = enc_str.replace('-_-', '/')
            aes_obj = AES.new(
                hashlib.sha256(str_key.encode()).digest(), AES.MODE_CFB, self.salt
            )
            str_tmp = b64decode(enc_str.encode(self.enc_dec_method))
            str_dec = aes_obj.decrypt(str_tmp)
            mret = str_dec.decode(self.enc_dec_method)
            return mret
        except ValueError as value_error:
            if value_error.args[0] == 'IV must be 16 bytes long':
                raise ValueError('Decryption Error: SALT must be 16 characters long')
            elif (
                value_error.args[0] == 'AES key must be either 16, 24, or 32 bytes long'
            ):
                raise ValueError(
                    'Decryption Error: Encryption key must be either 16, 24, or 32 characters long'
                )
            else:
                raise ValueError(value_error)


def encode(string: str, secret: Optional[str] = None):
    if not secret:
        secret = settings.SECRET_KEY
    c = __Crypt()
    return c.encrypt(string, secret)


def decode(enc: str, secret: Optional[str] = None):
    if not secret:
        secret = settings.SECRET_KEY
    c = __Crypt()
    return c.decrypt(enc, secret)


def write_ram_file(
    f: StringIO, data: Generator, fieldnames: list, delimiter='\t'
) -> StringIO:
    writer = csv.DictWriter(f, delimiter=delimiter, fieldnames=fieldnames)
    writer.writeheader()
    for row in data:
        writer.writerow(row)
    return f


def upload_to_s3_from_ram(
    content: Union[StringIO, BytesIO],
    filename: str,
    folder: str = 'yandex_files/',
    suffix: str = '.tsv',
):
    if filename.startswith('/tmp/'):
        s3_filename = filename[5:]
    else:
        s3_filename = filename
    if suffix not in s3_filename:
        s3_filename = f"{s3_filename}{suffix}"
    s3 = boto3.resource('s3')
    if folder.startswith('/'):
        folder = folder[1:]
    if not folder.endswith('/'):
        folder = f'{folder}/'
    body = (
        content.getvalue().encode('utf-8')
        if isinstance(content, StringIO)
        else content.getvalue()
    )
    s3.meta.client.put_object(
        Bucket=BUCKET_NAME, Key=f'{folder}{s3_filename}', Body=body, ACL='public-read'
    )
    return {"status": "success", "s3_filename": s3_filename, "s3_folder": folder}


def delete_invalid_integrations(
    integrations: list, models: Union[tuple, list], filter_query: Optional[dict] = None
) -> list:
    integration_ids = [i['integration_id'] for i in integrations]
    return [
        model.objects.exclude(integration_id__in=integration_ids).delete()
        if not filter_query
        else model.objects.filter(**filter_query)
        .exclude(integration_id__in=integration_ids)
        .delete()
        for model in models
    ]


def decrypt_data(data: dict, token: str, salt: Optional[str] = None) -> dict:
    if not salt:
        salt = settings.EXECUTE_TOKEN
    try:
        execute_token = f'{token}:{salt}'
        data = decode(data, execute_token)
        return json.loads(data)
    except:
        raise ValueError('invalid secure params')


def dates_chunker(
    date_from: datetime, date_to: datetime, default_delta: int = 4
) -> Generator:
    """Return dataes chunker like [[date1, date2]]

    Args:
        date_from (datetime): from date
        date_to (datetime): to date
        default_delta (int, optional): date range. Defaults to 4.

    Yields:
        Generator: dates generator
    """
    dates_delta = (date_to - date_from).days
    for count in range(0, dates_delta + 1, default_delta):
        if count + default_delta > dates_delta:
            default_delta = dates_delta - count + 1
        yield [
            date_from,
            (date_from + timedelta(days=default_delta - 1)),
        ]
        date_from = date_from + timedelta(days=default_delta)

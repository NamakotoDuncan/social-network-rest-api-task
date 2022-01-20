import logging
import os
from datetime import datetime
from pathlib import Path

import environ
import requests
from celery import shared_task
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .models import CustomUser

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

logger = logging.getLogger(__name__)

MAX_RETRY = 3
MAX_RETRY_FOR_SESSION = 2
BACK_OFF_FACTOR = 0.3
TIME_BETWEEN_RETRIES = 30000
ERROR_CODES = (500, 502, 504)


def requests_retry_session(retries=MAX_RETRY_FOR_SESSION,
                           back_off_factor=BACK_OFF_FACTOR,
                           status_force_list=ERROR_CODES,
                           session=None):
    session = session
    retry = Retry(total=retries, read=retries, connect=retries,
                  backoff_factor=back_off_factor,
                  status_forcelist=status_force_list,
                  method_whitelist=frozenset(['GET', 'POST']))
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


@shared_task
def prepare_and_submit_data(email):
    # https://github.com/SrinivasK438/tradecore-testtask/blob/main/users/abstractapi.py
    user = CustomUser.objects.get(email=email)
    logger.info(email)
    validate_email(email, user.id)
    geo_ip_data(user.id)


def validate_email(email, user_id):
    user = CustomUser.objects.get(id=user_id)
    session = requests_retry_session(session=requests.Session())
    url = "{0}{1}&email={1}".format(env('EMAIL_VALIDATION_ENDPOINT'), env('ABSTRACT_EMAIL_VALIDATION_API_KEY'), email)
    response = session.get(url).json()
    logger.info('quality score'.format(response['quality_score']))
    user.email_valid = float(response['quality_score']) > 0.7
    user.save()


def geo_ip_data(user_id):
    user = CustomUser.objects.get(id=user_id)
    ip_address = user.ip_address
    session = requests_retry_session(session=requests.Session())
    url = "{0}{1}&ip_address={2}".format(env('GEO_IP_ENDPOINT'), env('ABSTRACT_API_GEO_IP_KEY'), ip_address)
    response = session.get(url).json()
    user.country = response['country']
    user.save()
    date = datetime.strptime(user.date_joined, "%Y-%m-%dT%H:%M:%S.%fZ")
    day = date.day
    month = date.month
    year= date.year
    holiday_data(user_id, country=response['country'], year=year, month=month, day=day)


def holiday_data(user_id, country, year, month, day):
    logger.info('Country {0}'.format(country))
    user = CustomUser.objects.get(id=user_id)
    session = requests_retry_session(session=requests.Session())
    url = "{0}{1}&country={2}&year={3}&month={4}&day={5}".format(env('HOLIDAY_ENDPOINT'),
                                                                 env('ABSTRACT_API_HOLIDAY_KEY'),
                                                                 country, year, month, day)
    response = session.get(url).json()
    logger.warning(str(response))
    user.joined_on_holiday = response.length > 0
    user.save()

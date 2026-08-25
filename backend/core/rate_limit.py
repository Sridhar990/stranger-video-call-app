from slowapi import Limiter
from slowapi.util import get_remote_address

from core.settings import TESTING

limiter = Limiter(key_func=get_remote_address)

if TESTING:
    limiter.enabled = False
import jwt
import logging

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
User = get_user_model()
logger = logging.getLogger(__name__)

formatter = logging.Formatter('%(asctime)s %(levelname)s - %(message)s')

# 文件日志
file_handler = logging.FileHandler("verify_jwt.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO) #set log level

pem_pub_list = list()

default_pub_pem = """
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAt+F0UUMjH50ZQ0HwH+hs
jXaz0Ro25MkJFVMEYNFBo9O7+0LynpcaoL06lbXgQc2LhWm086/EMjFNYpjgX2p7
OWDBbdwQ0C9gEmqPS9m4IqpporsOQvqn1h9Zi1BFmGZCwJBjs+QSz/9U5LSGYmk8
hpcLpSUuJhAeffSo7eyBOg97e+QUSOo8j0w/7yd7B1Q9MAiCeWYSkNfVWrd6VmFi
SMY5F20p6pDRY+WkeiBrvZbuKM8WlznpTG/0eQDfL3T5/vlIIeXJUoJRDGkMX8pL
nTVnRCKwUccQ7lIViVR5oOi/fQfDHC8vK3ggvj+0i0TCo/sSj5mJnknvPsm7dZU6
zQIDAQAB
-----END PUBLIC KEY-----
"""


if hasattr(settings, "PUBLIC_PEM"):
    pem_pub_list.append(settings.PUBLIC_PEM)

pem_pub_list.append(default_pub_pem)



class Auth(MiddlewareMixin):

    def process_request(self, request):
        if not hasattr(settings, "LOGIN_URL") or not hasattr(settings, "LOGOUT_URL"):
            raise Exception("please config LOGIN_URL and LOGOUT_URL")
        if request.path != settings.LOGIN_URL and request.path != settings.LOGOUT_URL:
            jwt_user = SimpleLazyObject(lambda: self.get_jwt_user(request))
            jwt_test = str(request.COOKIES.get('test'))
            if jwt_test == '1':
                logger.info('test=1,use jwt user:' + str(jwt_user.username))
                request.user = jwt_user
            else:
                if not isinstance(jwt_user, AnonymousUser):
                    request.user = jwt_user

    def get_jwt_user(self, request):
        token = request.META.get("HTTP_JWTAUTHORIZATION")
        if not token:
            return AnonymousUser()
        try:
            payload = self.verify_token(token[7:])
        except:
            logger.info('verify jwt error:token:' + token)
            return AnonymousUser()
        username = payload.get('username')
        try:
            user = User.objects.get(username=username)
            if user:
                logger.info('verify jwt:' + str(user.username))
                return user
        except:
            return AnonymousUser()
        return AnonymousUser()

    def verify_token(self, token):
        """
        对token进行解码
        :param token:
        :return:
        """
        for pem in pem_pub_list:
            try:
                payload = jwt.decode(token, pem, algorithms=['RS256'])
                return payload
            except:
                continue
        raise Exception("starmerx JWT error")


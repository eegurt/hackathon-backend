import ssl
from django.core.mail.backends.smtp import EmailBackend


class UnsafeEmailBackend(EmailBackend):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # отключаем проверку сертификата
        self.ssl_context = ssl._create_unverified_context()
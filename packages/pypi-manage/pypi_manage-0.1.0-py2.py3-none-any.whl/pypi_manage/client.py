from pypi_manage.session import PypiSession
from pypi_manage.tokens import Tokens


class PypiClient:
    def __init__(self, session: PypiSession):
        self.session = session

    @property
    def tokens(self):
        return Tokens(self.session)

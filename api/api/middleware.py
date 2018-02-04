from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

from api.settings import LEGACY_SESSION


class SQLAlchemySessionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.db_session = LEGACY_SESSION()

    def process_response(self, request, response):
        try:
            session = request.db_session
        except AttributeError:
            return response
        try:
            session.commit()
            return response
        except:
            session.rollback()
            raise

    def process_exception(self, request, exception):
        try:
            session = request.db_session
        except AttributeError:
            return
        session.rollback()
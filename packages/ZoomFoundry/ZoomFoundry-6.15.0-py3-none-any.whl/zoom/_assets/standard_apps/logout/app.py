"""
    zoom.logout
"""

import logging

from zoom.tools import redirect_to
from zoom.components import warning
from zoom.response import RedirectResponse


def app(request):
    logger = logging.getLogger(__name__)
    user = request.user

    as_api = request.env.get('HTTP_ACCEPT', '') == 'application/json'

    if not user.is_authenticated:
        if as_api:
            return '{"message": "not logged in"}'
        else:
            logger.debug('user %s is not logged in', user.username)
            warning('You are not logged in')
    else:

        user.logout()

        if as_api:
            logger.info('user %s successfully logged out via api', user.username)
            return 'null'
        else:
            logger.info('user %s successfully logged out', user.link)

    return RedirectResponse('/')

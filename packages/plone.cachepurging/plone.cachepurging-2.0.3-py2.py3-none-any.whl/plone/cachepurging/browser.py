# -*- coding: utf-8 -*-
from plone.cachepurging.interfaces import ICachePurgingSettings
from plone.cachepurging.interfaces import IPurger
from plone.cachepurging.utils import getPathsToPurge
from plone.cachepurging.utils import getURLsToPurge
from plone.cachepurging.utils import isCachePurgingEnabled
from plone.registry.interfaces import IRegistry
from six import StringIO
from z3c.caching.purge import Purge
from zope.component import getUtility
from zope.event import notify

RESULT_TPL = (
    "Purged: {url}, Status: {status}, X-Cache: {xcache}, Error: {xerror}\n"
)


class QueuePurge(object):
    """Manually initiate a purge
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):

        if not isCachePurgingEnabled():
            return "Caching not enabled"

        notify(Purge(self.context))
        return "Queued"


class PurgeImmediately(object):
    """Purge immediately
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        if not isCachePurgingEnabled():
            return "Caching not enabled"

        registry = getUtility(IRegistry)
        settings = registry.forInterface(ICachePurgingSettings)
        purger = getUtility(IPurger)
        out = StringIO()

        for path in getPathsToPurge(self.context, self.request):
            for url in getURLsToPurge(path, settings.cachingProxies):
                status, xcache, xerror = purger.purgeSync(url)
                out.write(
                    RESULT_TPL.format(
                        url=url, status=status, xcache=xcache, xerror=xerror
                    )
                )
        return out.getvalue()

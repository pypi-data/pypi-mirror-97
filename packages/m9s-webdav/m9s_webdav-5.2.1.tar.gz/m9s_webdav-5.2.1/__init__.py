# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import webdav

__all__ = ['register']


def register():
    Pool.register(
        webdav.Collection,
        webdav.Share,
        webdav.Attachment,
        module='webdav', type_='model')

# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.pool import Pool
from . import static_file
from . import website

__all__ = ['register']


def register():
    Pool.register(
        static_file.NereidStaticFile,
        website.WebSite,
        module='nereid_image_transformation', type_='model')

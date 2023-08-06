# -*- encoding: utf-8 -*-
"""
    flask_triangle.helpers.html
    ---------------------------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals

import sys


# compatibility with python 2.x and 3.x
if sys.version_info > (3, 0):
    base = str
else:
    base = unicode


class HTMLString(base):
    """
    The HTMLString object is a standard string ehanced with an __html__ method.
    It's content will render as is in the template.
    """

    def __html__(self):
        return self

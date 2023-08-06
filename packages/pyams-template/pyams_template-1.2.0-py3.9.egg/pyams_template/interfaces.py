#
# Copyright (c) 2008-2015 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_template.interfaces module

Templates marker interfaces definitions
"""

from zope.interface import Interface

__docformat__ = 'restructuredtext'


class IPageTemplate(Interface):
    """Base page template interface"""


class ILayoutTemplate(IPageTemplate):
    """A template used for render the layout."""


class IContentTemplate(IPageTemplate):
    """A template used for render the content."""

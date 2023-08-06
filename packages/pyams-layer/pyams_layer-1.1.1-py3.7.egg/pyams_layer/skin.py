#
# Copyright (c) 2015-2019 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_layer.skin module

This module provides base skin management tools.
"""

import logging

from pyramid.events import subscriber
from pyramid.threadlocal import get_current_request
from zope.interface import directlyProvidedBy, directlyProvides, implementer
from zope.schema.fieldproperty import FieldProperty
from zope.traversing.interfaces import IBeforeTraverseEvent

from pyams_file.property import FileProperty
from pyams_layer.interfaces import IBaseLayer, IPyAMSLayer, ISkin, ISkinnable, IUserSkinnable, \
    PYAMS_BASE_SKIN_NAME, SkinChangedEvent
from pyams_site.interfaces import ISiteRoot
from pyams_utils.interfaces.form import TO_BE_DELETED
from pyams_utils.registry import utility_config
from pyams_utils.request import check_request
from pyams_utils.traversing import get_parent
from pyams_utils.zodb import volatile_property


__docformat__ = 'restructuredtext'

from pyams_layer import _  # pylint: disable=ungrouped-imports


LOGGER = logging.getLogger('PyAMS (layer)')


@implementer(ISkinnable)
class SkinnableContentMixin:
    """Skinnable content base class"""

    _inherit_skin = FieldProperty(ISkinnable['inherit_skin'])
    _skin = FieldProperty(IUserSkinnable['skin'])

    _custom_stylesheet = FileProperty(ISkinnable['custom_stylesheet'])
    _editor_stylesheet = FileProperty(ISkinnable['editor_stylesheet'])
    _custom_script = FileProperty(ISkinnable['custom_script'])

    @property
    def can_inherit_skin(self):
        """Can we inherit skin from parent?"""
        return get_parent(self, ISkinnable, allow_context=False) is not None

    @property
    def inherit_skin(self):
        """Do we inherit skin from parent?"""
        return self._inherit_skin if self.can_inherit_skin else False

    @inherit_skin.setter
    def inherit_skin(self, value):
        """Change skin inheritance"""
        if self.can_inherit_skin:
            self._inherit_skin = value
        del self.skin_parent

    @property
    def no_inherit_skin(self):
        """Don't we inherit skin from parent?"""
        return not bool(self.inherit_skin)

    @no_inherit_skin.setter
    def no_inherit_skin(self, value):
        """Change skin inheritance"""
        self.inherit_skin = not bool(value)

    @volatile_property
    def skin_parent(self):
        """Get parent of current skin, which can be self if not inherited"""
        if (not self._inherit_skin) and self.skin:
            return self
        parent = get_parent(self, ISkinnable, allow_context=False)
        if parent is not None:
            return parent.skin_parent
        return None

    @property
    def skin(self):
        """Get current skin"""
        if not self.inherit_skin:
            return self._skin
        return self.skin_parent.skin  # pylint: disable=no-member

    @skin.setter
    def skin(self, value):
        """Set current skin"""
        if not self.inherit_skin:
            self._skin = value
        del self.skin_parent

    @property
    def custom_stylesheet(self):
        """Get custom stylesheet"""
        if not self.inherit_skin:
            return self._custom_stylesheet
        return self.skin_parent.custom_stylesheet  # pylint: disable=no-member

    @custom_stylesheet.setter
    def custom_stylesheet(self, value):
        """Set custom stylesheet"""
        if not self.inherit_skin:
            self._custom_stylesheet = value
            if value and (value is not TO_BE_DELETED):
                self._custom_stylesheet.content_type = 'text/css'

    @property
    def editor_stylesheet(self):
        """Get editor stylesheet"""
        if not self.inherit_skin:
            return self._editor_stylesheet
        return self.skin_parent.editor_stylesheet  # pylint: disable=no-member

    @editor_stylesheet.setter
    def editor_stylesheet(self, value):
        """Set editor stylesheet"""
        if not self.inherit_skin:
            self._editor_stylesheet = value
            if value and (value is not TO_BE_DELETED):
                self._editor_stylesheet.content_type = 'text/css'

    @property
    def custom_script(self):
        """Get custom script"""
        if not self.inherit_skin:
            return self._custom_script
        return self.skin_parent.custom_script  # pylint: disable=no-member

    @custom_script.setter
    def custom_script(self, value):
        """Set custom script"""
        if not self.inherit_skin:
            self._custom_script = value
            if value and (value is not TO_BE_DELETED):
                self._custom_script.content_type = 'text/javascript'

    def get_skin(self, request=None):
        """Get skin utility matching current settings"""
        parent = self.skin_parent
        if parent is not None:
            if request is None:
                request = get_current_request()
            return request.registry.queryUtility(ISkin, parent.skin)  # pylint: disable=no-member
        return None


@implementer(IUserSkinnable)
class UserSkinnableContentMixin(SkinnableContentMixin):
    """User skinnable content base class"""


def get_layer_skin(layer):
    """Get skin matching given layer"""
    request = check_request()
    registry = request.registry
    for name, util in registry.getUtilitiesFor(ISkin):  # pylint: disable=unused-variable
        if util.layer is layer:
            return util
    return None


def apply_skin(request, skin):
    """Apply given skin to request"""

    def _apply(request, skin):
        """Apply skin to request"""
        ifaces = [iface for iface in directlyProvidedBy(request)
                  if not issubclass(iface, IBaseLayer)]
        # Add the new skin.
        ifaces.append(skin.layer)
        directlyProvides(request, *ifaces)
        LOGGER.debug("Applied skin {0!r} to request {1!r}".format(skin.label, request))

    if isinstance(skin, str):
        skin = request.registry.queryUtility(ISkin, skin)
    if skin is not None:
        _apply(request, skin)
        request.registry.notify(SkinChangedEvent(request))
        try:
            request.annotations['__skin__'] = skin
        except AttributeError:
            pass


def get_skin(request):
    """Get skin applied on request"""
    try:
        return request.annotations['__skin__']
    except AttributeError:
        ifaces = [iface for iface in directlyProvidedBy(request)
                  if issubclass(iface, IBaseLayer)]
        if ifaces:
            return get_layer_skin(ifaces[0])
    return None


@subscriber(IBeforeTraverseEvent, context_selector=ISkinnable)
def handle_content_skin(event):
    """Apply skin when traversing skinnable object"""
    request = event.request
    skinnable = event.object
    if not skinnable.inherit_skin:
        skin = skinnable.get_skin(request)
        if skin is not None:
            apply_skin(request, skin)


@subscriber(IBeforeTraverseEvent, context_selector=ISiteRoot)
def handle_root_skin(event):
    """Apply skin when traversing site root"""
    context = event.object
    if (not ISkinnable.providedBy(context)) or (context.skin is None):
        apply_skin(event.request, PyAMSSkin)


#
# Base default skin
#

@utility_config(name=PYAMS_BASE_SKIN_NAME, provides=ISkin)
class PyAMSSkin:
    """PyAMS base skin"""

    label = _("PyAMS base skin")
    layer = IPyAMSLayer

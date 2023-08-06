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

"""PyAMS_file.property module

This module defines files properties which can be used to automatically handle all the magic
behind external files management; this includes blobs management and their references counting.
"""

from pyramid.events import subscriber
from pyramid.threadlocal import get_current_registry
from zope.interface import alsoProvides
from zope.lifecycleevent import IObjectRemovedEvent, ObjectAddedEvent, ObjectCreatedEvent, \
    ObjectRemovedEvent
from zope.location import locate
from zope.schema.interfaces import IField

from pyams_file.file import FileFactory
from pyams_file.interfaces import FILE_CONTAINER_ATTRIBUTES, IFile, IFileFieldContainer, IFileInfo
from pyams_utils.adapter import get_annotation_adapter
from pyams_utils.interfaces.form import NOT_CHANGED, TO_BE_DELETED


__docformat__ = 'restructuredtext'


_MARKER = object()


def get_instance_attributes(instance):
    """Get file attributes of given instance"""
    return get_annotation_adapter(instance, FILE_CONTAINER_ATTRIBUTES, set,
                                  notify=False, locate=False)


class FileProperty:
    """Property class used to handle files"""

    def __init__(self, field, name=None, klass=None, **args):
        if not IField.providedBy(field):
            raise ValueError("Provided field must implement IField interface...")
        if name is None:
            name = field.__name__
        self.__field = field
        self.__name = name
        self.__klass = klass
        self.__args = args

    def __get__(self, instance, klass):
        if instance is None:
            return self
        value = instance.__dict__.get(self.__name, _MARKER)
        if value is _MARKER:
            field = self.__field.bind(instance)
            value = getattr(field, 'default', _MARKER)
            if value is _MARKER:
                raise AttributeError(self.__name)
        return value

    def __set__(self, instance, value):  # pylint: disable=too-many-branches
        if value is NOT_CHANGED:
            return
        registry = get_current_registry()
        if (value is not None) and (value is not TO_BE_DELETED):
            filename = None
            # file upload data converter returns a tuple containing
            # filename and buffered IO stream extracted from FieldStorage...
            if isinstance(value, tuple):
                filename, value = value
            # initialize file through factory
            if not IFile.providedBy(value):
                factory = self.__klass or FileFactory
                file = factory(value, **self.__args)
                registry.notify(ObjectCreatedEvent(file))
                if not file.get_size():
                    value.seek(0)  # because factory may read until end of file...
                    file.data = value
                value = file
            if filename is not None:
                info = IFileInfo(value)
                if info is not None:
                    info.filename = filename
        field = self.__field.bind(instance)
        field.validate(value)
        if field.readonly and instance.__dict__.has_key(self.__name):
            raise ValueError(self.__name, "Field is readonly")
        old_value = instance.__dict__.get(self.__name, _MARKER)
        if old_value != value:
            # check for previous value
            if (old_value is not _MARKER) and (old_value is not None):
                registry.notify(ObjectRemovedEvent(old_value))
            if value is TO_BE_DELETED:
                if self.__name in instance.__dict__:
                    del instance.__dict__[self.__name]
                attributes = get_instance_attributes(instance)
                if attributes and (self.__name in attributes):
                    attributes.remove(self.__name)
            else:
                # set name of new value
                name = '++attr++{0}'.format(self.__name)
                if value is not None:
                    locate(value, instance, name)
                instance.__dict__[self.__name] = value
                # store file attributes of instance
                if not IFileFieldContainer.providedBy(instance):
                    alsoProvides(instance, IFileFieldContainer)
                attributes = get_instance_attributes(instance)
                attributes.add(self.__name)
                registry.notify(ObjectAddedEvent(value, instance, name))

    def __delete__(self, instance):
        old_value = instance.__dict__.get(self.__name, _MARKER)
        if (old_value is not _MARKER) and (old_value is not None):
            registry = get_current_registry()
            registry.notify(ObjectRemovedEvent(old_value))
        attributes = get_instance_attributes(instance)
        if attributes and (self.__name in attributes):
            attributes.remove(self.__name)
        del instance.__dict__[self.__name]


class I18nFileProperty:
    """I18n property class used to handle files"""

    def __init__(self, field, name=None, klass=None, **args):
        if not IField.providedBy(field):
            raise ValueError("Provided field must implement IField interface...")
        if name is None:
            name = field.__name__
        self.__field = field
        self.__name = name
        self.__klass = klass
        self.__args = args

    def __get__(self, instance, klass):
        if instance is None:
            return self
        value = instance.__dict__.get(self.__name, _MARKER)
        if value is _MARKER:
            field = self.__field.bind(instance)
            value = getattr(field, 'default', _MARKER)
            if value is _MARKER:
                raise AttributeError(self.__name)
        return value

    def __set__(self, instance, value):
        # pylint: disable=too-many-locals,too-many-statements,too-many-branches
        registry = get_current_registry()
        for lang in value:
            lang_value = value[lang]
            if (lang_value is TO_BE_DELETED) or (lang_value is NOT_CHANGED):
                continue
            if lang_value is not None:
                filename = None
                # file upload data converter returns a tuple containing
                # filename and buffered IO stream extracted from FieldStorage...
                if isinstance(lang_value, tuple):
                    filename, lang_value = lang_value
                # initialize file through factory
                if not IFile.providedBy(lang_value):
                    factory = self.__klass or FileFactory
                    file = factory(lang_value, **self.__args)
                    registry.notify(ObjectCreatedEvent(file))
                    if not file.get_size():
                        lang_value.seek(0)  # because factory may read until end of file...
                        file.data = lang_value
                    lang_value = file
                if filename is not None:
                    info = IFileInfo(lang_value)
                    if info is not None:
                        info.filename = filename
            value[lang] = lang_value
        field = self.__field.bind(instance)
        field.validate(value)
        if field.readonly and instance.__dict__.has_key(self.__name):
            raise ValueError(self.__name, "Field is readonly")
        old_value = instance.__dict__.get(self.__name, _MARKER)
        if old_value != value:
            # check for previous value
            if old_value is _MARKER:
                old_value = {}
            for lang in value:
                new_lang_value = value.get(lang)
                if new_lang_value is NOT_CHANGED:
                    continue
                old_lang_value = old_value.get(lang, _MARKER)
                if (old_lang_value is not _MARKER) and (old_lang_value is not None):
                    registry.notify(ObjectRemovedEvent(old_lang_value))
                attrname = '{0}::{1}'.format(self.__name, lang)
                if new_lang_value is TO_BE_DELETED:
                    if (self.__name in instance.__dict__) and (lang in old_value):
                        del old_value[lang]
                    attributes = get_instance_attributes(instance)
                    if attributes and (attrname in attributes):
                        attributes.remove(attrname)
                else:
                    # set name of new value
                    name = '++i18n++{0}:{1}'.format(self.__name, lang)
                    if new_lang_value is not None:
                        locate(new_lang_value, instance, name)
                    old_value[lang] = new_lang_value
                    # store file attributes of instance
                    if not IFileFieldContainer.providedBy(instance):
                        alsoProvides(instance, IFileFieldContainer)
                    attributes = get_instance_attributes(instance)
                    attributes.add(attrname)
                    registry.notify(ObjectAddedEvent(new_lang_value, instance, name))
            instance.__dict__[self.__name] = old_value

    def __delete__(self, instance):
        attributes = get_instance_attributes(instance)
        old_value = instance.__dict__.get(self.__name, _MARKER)
        if (old_value is not _MARKER) and (old_value is not None):
            registry = get_current_registry()
            for lang in list(old_value):
                old_lang_value = old_value.get(lang, _MARKER)
                if (old_lang_value is not _MARKER) and (old_lang_value is not None):
                    registry.notify(ObjectRemovedEvent(old_lang_value))
                    del old_value[lang]
                attrname = '{0}::{1}'.format(self.__name, lang)
                if attributes and (attrname in attributes):
                    attributes.remove(attrname)
        del instance.__dict__[self.__name]


@subscriber(IObjectRemovedEvent, context_selector=IFileFieldContainer)
def handle_removed_file_container(event):
    """Handle removal of files containers"""
    instance = event.object
    attributes = get_instance_attributes(instance)
    for attr in attributes.copy():
        if '::' in attr:
            attr, lang = attr.split('::')  # pylint:disable=unused-variable
        delattr(instance, attr)

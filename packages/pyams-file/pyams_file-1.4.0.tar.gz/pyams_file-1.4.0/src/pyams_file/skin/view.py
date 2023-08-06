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

"""PyAMS_file.skin.view module

This module provides a Pyramid view used to download any file.
"""

from http.client import NOT_MODIFIED, PARTIAL_CONTENT

from pyramid.response import Response
from pyramid.view import view_config
from zope.dublincore.interfaces import IZopeDublinCore

from pyams_file.interfaces import IFile
from pyams_utils.unicode import translate_string


__docformat__ = 'restructuredtext'


MAX_RANGE_LENGTH = 1 << 21  # 2 Mb


@view_config(context=IFile)
def FileView(request):  # pylint: disable=invalid-name
    """Default file view"""
    context = request.context

    # set content type
    content_type = context.content_type
    if isinstance(content_type, bytes):
        content_type = content_type.decode('utf-8')

    # check for last modification date
    response = Response(content_type=content_type)
    zdc = IZopeDublinCore(context, None)
    if zdc is not None:
        modified = zdc.modified
        if modified is not None:
            if_modified_since = request.if_modified_since
            # pylint: disable=no-member
            if if_modified_since and \
                    (int(modified.timestamp()) <= int(if_modified_since.timestamp())):
                return Response(content_type=content_type,
                                status=NOT_MODIFIED)
            response.last_modified = modified

    body_file = context.get_blob(mode='c')

    if request.params.get('dl') is not None:
        filename = context.filename or 'noname.txt'
        response.content_disposition = 'attachment; filename="{0}"'.format(
            translate_string(filename, force_lower=False))

    # check for range request
    if request.range is not None:
        try:
            body = body_file.read()
            body_length = len(body)
            range_start = request.range.start or 0
            if 'Firefox' in request.user_agent:  # avoid partial range for Firefox videos
                range_end = body_length
            else:
                range_end = request.range.end or min(body_length, range_start + MAX_RANGE_LENGTH)
            ranged_body = body[range_start:range_end]
            response.status = PARTIAL_CONTENT
            response.headers['Content-Range'] = 'bytes {first}-{last}/{len}'.format(
                first=range_start, last=range_start + len(ranged_body) - 1, len=body_length)
            response.body = ranged_body
        finally:
            body_file.close()
    else:
        response.body_file = body_file

    return response

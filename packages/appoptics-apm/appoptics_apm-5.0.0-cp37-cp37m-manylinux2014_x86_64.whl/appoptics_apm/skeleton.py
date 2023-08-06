# Modified from https://github.com/dcrosta/professor/blob/master/professor/skeleton.py
#
# Copyright (c) 2011, Daniel Crosta
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
import logging
import re
from datetime import datetime

import six
from bson.code import Code
from bson.dbref import DBRef
from bson.objectid import ObjectId
from bson.son import SON

logger = logging.getLogger(__name__)

__all__ = ('skeleton', 'sanitize')

BSON_TYPES = (
    set(six.integer_types) | set(six.string_types)
    | set([
        bool,
        float,
        datetime,
        ObjectId,
        type(re.compile('')),
        Code,
        type(None),
        DBRef,
        SON,
    ]))


def skeleton(query_part, preserve_first=False, keep_values=False, no_wrap=False):
    # >>> skeleton({u'acronym': u'AMSHAT'})
    # u'{acronym}'
    # >>> skeleton({u'_id': 1, u'locked': False})
    # u'{_id,locked}'
    # >>> skeleton({})
    # u'{}'
    # >>> skeleton({u'op': u'query'})
    # u'{op}'
    t = type(query_part)

    if t == SON:
        query_part = query_part.to_dict()
        t = type(query_part)
    elif query_part is None:
        query_part = ''
        t = type(query_part)

    if t == list:
        out = []
        for element in query_part:
            if preserve_first:
                sub = skeleton(element, keep_values=True)
                preserve_first = False
            else:
                sub = skeleton(element)
            if sub is not None:
                out.append(sub)
        if no_wrap:
            return six.u(','.join(out))
        else:
            return six.u('[{o}]'.format(o=','.join(out)))
    elif t == dict:
        out = []
        for key in sorted(query_part.keys()):
            sub = skeleton(query_part[key], keep_values=keep_values)
            if sub is not None:
                out.append('%s:%s' % (key, sub))
            else:
                out.append(key)
        if no_wrap:
            return six.u(','.join(out))
        else:
            return six.u('{%s}' % ','.join(out))
    elif keep_values:
        return str(query_part)
    elif t not in BSON_TYPES:
        logger.debug('Value: {} is of an unsupported type.'.format(query_part))
    return None


def sanitize(value):
    # return a copy of the query with all
    # occurrences of "$" replaced by "_$_",
    # and ocurrences of "." replaced by
    # "_,_" in keys
    t = type(value)
    if t == list:
        return map(sanitize, value)
    elif t == dict:
        return dict((k.replace('$', '_$_').replace('.', '_,_'), sanitize(v)) for k, v in value.items())
    elif t not in BSON_TYPES:
        logger.debug('Value: {} is of an unsupported type.'.format(value))
        return None
    else:
        return value


def desanitize(value):
    # perform the inverse of sanitize()
    t = type(value)
    if t == list:
        return map(desanitize, value)
    elif t == dict:
        return dict((k.replace('_$_', '$').replace('_,_', '.'), desanitize(v)) for k, v in value.items())
    elif t not in BSON_TYPES:
        logger.debug('Value: {} is of an unsupported type.'.format(value))
        return None
    else:
        return value

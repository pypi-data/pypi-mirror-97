#    Copyright 2021 SolarWinds, LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
""" AppOptics APM instrumentation for redis client module.
"""
import logging
import operator
import sys
from distutils.version import LooseVersion
from functools import wraps

from appoptics_apm import util

logger = logging.getLogger(__name__)
# which commands can we get hit/miss info from?
# also supports mget and hmget separately, see below
HITTABLE_COMMANDS = set(
    ('GET', 'GETSET', 'HGET', 'LINDEX', 'LGET', 'RPOPLPUSH', 'LPOP', 'RPOP', 'BRPOPLPUSH', 'SPOP', 'SRANDMEMBER'))

# which commands can we get KVKey from?
# for S*/H*/Z* commans, the key is currently the set/hash name
KEYABLE_COMMANDS = {
    'APPEND': 1,
    'BITCOUNT': 1,
    'BITOP': 2,  # XXX DEST
    'DECR': 1,
    'EXISTS': 1,
    'EXPIRE': 1,
    'EXPIREAT': 1,
    'GET': 1,
    'GETBIT': 1,
    'GETRANGE': 1,
    'GETSET': 1,
    'INCR': 1,
    'INCRBY': 1,
    'INCRBYFLOAT': 1,
    'MOVE': 1,
    'PEXPIRE': 1,
    'PEXPIREAT': 1,
    'PSETEX': 1,
    'PTTL': 1,
    'RENAME': 1,
    'RENAMEX': 1,
    'SET': 1,
    'SETBIT': 1,
    'SETEX': 1,
    'SETNX': 1,
    'SETRANGE': 1,
    'STRLEN': 1,
    'SUBSTR': 1,
    'TTL': 1,
    'TYPE': 1,
    'LINDEX': 1,
    'LINSERT': 1,
    'LLEN': 1,
    'LPOP': 1,
    'LPUSH': 1,
    'LPUSHX': 1,
    'LRANGE': 1,
    'LREM': 1,
    'LSET': 1,
    'LTRIM': 1,
    'RPOP': 1,
    'RPUSH': 1,
    'RPOPLPUSH': 1,
    'RPUSHX': 1,
    'SORT': 1,
    'SADD': 1,
    'SCARD': 1,
    'SDIFF': 1,
    'SDIFFSTORE': 1,  # XXX DEST
    'SINTERSTORE': 1,  # XXX DEST
    'SISMEMBER': 1,
    'SMEMBERS': 1,
    'SMOVE': 1,
    'SPOP': 1,
    'SRANDMEMBER': 1,
    'SREM': 1,
    'SUNIONSTORE': 1,  # XXX DEST
    'ZADD': 1,
    'ZCARD': 1,
    'ZCOUNT': 1,
    'ZINCRBY': 1,
    'ZINTERSTORE': 1,  # XXX DEST
    'ZRANGE': 1,
    'ZRANGEBYSCORE': 1,
    'ZRANK': 1,
    'ZREM': 1,
    'ZREMRANGEBYRANK': 1,
    'ZREMRANGEBYSCORE': 1,
    'ZREVRANGE': 1,
    'ZREVRANGEBYSCORE': 1,
    'ZREVRANK': 1,
    'ZSCORE': 1,
    'ZUNIONSCORE': 1,  # XXX DEST
    'HDEL': 1,
    'HEXISTS': 1,
    'HGET': 1,
    'HGETALL': 1,
    'HINCRBY': 1,
    'HINCRBYFLOAT': 1,
    'HKEYS': 1,
    'HLEN': 1,
    'HSET': 1,
    'HSETNX': 1,
    'HMSET': 1,
    'HMGET': 1,
    'HVALS': 1,
    'PUBLISH': 1  # CHANNEL
}

SCRIPT_COMMANDS = {
    'EVAL': 1,  # SCRIPT
    'EVALSHA': 1  # SHA
}

# these commands have two parts, as separate args in python redis client
# eg. SCRIPT LOAD
TWO_PARTERS = set(('SCRIPT', 'CLIENT', 'CONFIG', 'DEBUG'))


def wrap_execute_command(func, f_args, f_kwargs, return_val):
    """ This is where most "normal" redis commands are instrumented. """
    kvs = {}

    # command
    op = f_args[1]
    if op in TWO_PARTERS:
        op = op + ' ' + f_args[2]
    kvs['KVOp'] = op.lower()

    # key
    if op in KEYABLE_COMMANDS:
        kvs['KVKey'] = f_args[1 + KEYABLE_COMMANDS[op]]

    # script eval
    if op in SCRIPT_COMMANDS:
        kvs['Script'] = f_args[1 + SCRIPT_COMMANDS[op]][0:100]  # max out at 100 chars if script

    # hit/miss
    if op in HITTABLE_COMMANDS:
        kvs['KVHit'] = return_val is not None
    elif op in ('MGET', 'HMGET'):
        kvs['KVKeyCount'] = len(return_val)
        kvs['KVHitCount'] = sum(r is not None for r in return_val)

    return kvs


def wrap_execute_pipeline(func, f_args, f_kwargs, return_val):
    # args: self, connection, commands, raise_on_error
    kvs = {}
    fp_cmds = {}
    load_redis = sys.modules['redis']
    if load_redis is None:
        logger.warning('Failed to load module: {m}'.format(m='redis'))
        return kvs

    #redis version[2.4.0, 2.6.0] process args different from [2.6.0, ]
    if LooseVersion(load_redis.__version__) < LooseVersion("2.6.0") and \
       LooseVersion(load_redis.__version__) >= LooseVersion("2.4.0"):
        for (args, _) in f_args[1]:
            fp_cmds[args[0]] = fp_cmds.get(args[0], 0) + 1

        op = 'PIPE:' + ','.join([cmd for (cmd, _) in sorted(fp_cmds.items(), key=operator.itemgetter(0))])
        kvs['KVOp'] = op.lower()
    else:
        for (args, _) in f_args[2]:
            fp_cmds[args[0]] = fp_cmds.get(args[0], 0) + 1

        op = 'PIPE:' + ','.join([cmd for (cmd, _) in sorted(fp_cmds.items(), key=operator.itemgetter(0))])
        kvs['KVOp'] = op.lower()

    return kvs


def wrap_send_packed_command(layer_name, func):
    """ This is where we get the RemoteHost.

    This relies on the module internals, and just sends an info event when this
    function is called.
    """
    @wraps(func)  # XXX Not Python2.4-friendly
    def wrapper(*f_args, **f_kwargs):
        ret = func(*f_args, **f_kwargs)
        try:
            conn_obj = f_args[0]
            if 'path' in dir(conn_obj):
                host = 'localhost'
            else:
                host = conn_obj.host + ':' + str(conn_obj.port)

            util.log('info', layer_name, keys={'RemoteHost': host}, store_backtrace=util._collect_backtraces('redis'))
        except Exception as e:
            logger.error('AppOptics APM error: {e}'.format(e=e))
        return ret

    return wrapper


def wrap(layer_name, module):
    try:
        # first get the basic client methods; common point of processing is execute_command
        # client is StrictRedis for >= 2.4.10, or Redis for < 2.4.10
        cls = getattr(module, 'StrictRedis', getattr(module, 'Redis', None))
        if cls:
            execute_command = cls.execute_command
            wrapper = util.log_method(layer_name, callback=wrap_execute_command)
            setattr(cls, 'execute_command', wrapper(execute_command))
        else:
            logger.error(
                "AppOptics APM error: couldn't find redis.StrictRedis nor redis.Redis class to"
                " instrument, redis coverage may be partial.")

        # RemoteHost
        cls = getattr(module, 'Connection', None)
        if cls:
            wrapper = wrap_send_packed_command(layer_name, cls.send_packed_command)
            setattr(cls, 'send_packed_command', wrapper)
        else:
            logger.error(
                "AppOptics APM error: couldn't find redis.Connection class to instrument, "
                "redis coverage may be partial.")

        # pipeline/multi
        cls = getattr(module.client, 'BasePipeline', getattr(module.client, 'Pipeline', None))
        if cls:
            wrapper = util.log_method(layer_name, callback=wrap_execute_pipeline)
            execute_pipeline = cls._execute_pipeline
            setattr(cls, '_execute_pipeline', wrapper(execute_pipeline))
            execute_transaction = cls._execute_transaction
            setattr(cls, '_execute_transaction', wrapper(execute_transaction))
        else:
            logger.error(
                "AppOptics APM error: couldn't find redis.client.BasePipeline nor "
                "redis.client.Pipeline class to instrument, "
                "redis coverage may be partial.")

        # pubsub
        cls = getattr(module.client, 'PubSub', None)
        if cls:
            execute_command = cls.execute_command
            wrapper = util.log_method(layer_name, callback=wrap_execute_command)
            setattr(cls, 'execute_command', wrapper(execute_command))
        else:
            logger.error(
                "AppOptics APM error: couldn't find redis.client.PubSub class to instrument, "
                "redis coverage may be partial.")

    except Exception as e:
        logger.error("AppOptics APM error: {e}".format(e=e))


if util.ready():
    try:
        import redis

        wrap('redis', redis)
    except ImportError as ex:
        pass

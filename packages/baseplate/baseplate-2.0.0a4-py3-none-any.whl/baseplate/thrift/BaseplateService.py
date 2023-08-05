#
# Autogenerated by Thrift Compiler (0.14.1)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py:slots
#
import logging
import sys

from thrift.protocol.TProtocol import TProtocolException
from thrift.Thrift import TApplicationException
from thrift.Thrift import TException
from thrift.Thrift import TFrozenDict
from thrift.Thrift import TMessageType
from thrift.Thrift import TProcessor
from thrift.Thrift import TType
from thrift.transport import TTransport
from thrift.TRecursive import fix_spec

from .ttypes import *

all_structs = []


class Iface(object):
    """
    The base for any baseplate-based service.

    Your service should inherit from this one so that common tools can interact
    with any expected interfaces.

    DEPRECATED: Please migrate to BaseplateServiceV2.


    """

    def is_healthy(self):
        """
        Return whether or not the service is healthy.

        The healthchecker (baseplate.server.healthcheck) expects this endpoint to
        exist so it can determine your service's health.

        This should return True if the service is healthy. If the service is
        unhealthy, it can return False or raise an exception.


        """
        pass


class Client(Iface):
    """
    The base for any baseplate-based service.

    Your service should inherit from this one so that common tools can interact
    with any expected interfaces.

    DEPRECATED: Please migrate to BaseplateServiceV2.


    """

    def __init__(self, iprot, oprot=None):
        self._iprot = self._oprot = iprot
        if oprot is not None:
            self._oprot = oprot
        self._seqid = 0

    def is_healthy(self):
        """
        Return whether or not the service is healthy.

        The healthchecker (baseplate.server.healthcheck) expects this endpoint to
        exist so it can determine your service's health.

        This should return True if the service is healthy. If the service is
        unhealthy, it can return False or raise an exception.


        """
        self.send_is_healthy()
        return self.recv_is_healthy()

    def send_is_healthy(self):
        self._oprot.writeMessageBegin("is_healthy", TMessageType.CALL, self._seqid)
        args = is_healthy_args()
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_is_healthy(self):
        iprot = self._iprot
        (fname, mtype, rseqid) = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = is_healthy_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        raise TApplicationException(
            TApplicationException.MISSING_RESULT, "is_healthy failed: unknown result"
        )


class Processor(Iface, TProcessor):
    def __init__(self, handler):
        self._handler = handler
        self._processMap = {}
        self._processMap["is_healthy"] = Processor.process_is_healthy
        self._on_message_begin = None

    def on_message_begin(self, func):
        self._on_message_begin = func

    def process(self, iprot, oprot):
        (name, type, seqid) = iprot.readMessageBegin()
        if self._on_message_begin:
            self._on_message_begin(name, type, seqid)
        if name not in self._processMap:
            iprot.skip(TType.STRUCT)
            iprot.readMessageEnd()
            x = TApplicationException(
                TApplicationException.UNKNOWN_METHOD, "Unknown function %s" % (name)
            )
            oprot.writeMessageBegin(name, TMessageType.EXCEPTION, seqid)
            x.write(oprot)
            oprot.writeMessageEnd()
            oprot.trans.flush()
            return
        else:
            self._processMap[name](self, seqid, iprot, oprot)
        return True

    def process_is_healthy(self, seqid, iprot, oprot):
        args = is_healthy_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = is_healthy_result()
        try:
            result.success = self._handler.is_healthy()
            msg_type = TMessageType.REPLY
        except TTransport.TTransportException:
            raise
        except TApplicationException as ex:
            logging.exception("TApplication exception in handler")
            msg_type = TMessageType.EXCEPTION
            result = ex
        except Exception:
            logging.exception("Unexpected exception in handler")
            msg_type = TMessageType.EXCEPTION
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, "Internal error")
        oprot.writeMessageBegin("is_healthy", msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()


# HELPER FUNCTIONS AND STRUCTURES


class is_healthy_args(object):

    __slots__ = ()

    def read(self, iprot):
        if (
            iprot._fast_decode is not None
            and isinstance(iprot.trans, TTransport.CReadableTransport)
            and self.thrift_spec is not None
        ):
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin("is_healthy_args")
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ["%s=%r" % (key, getattr(self, key)) for key in self.__slots__]
        return "%s(%s)" % (self.__class__.__name__, ", ".join(L))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        for attr in self.__slots__:
            my_val = getattr(self, attr)
            other_val = getattr(other, attr)
            if my_val != other_val:
                return False
        return True

    def __ne__(self, other):
        return not (self == other)


all_structs.append(is_healthy_args)
is_healthy_args.thrift_spec = ()


class is_healthy_result(object):
    """
    Attributes:
     - success

    """

    __slots__ = ("success",)

    def __init__(
        self, success=None,
    ):
        self.success = success

    def read(self, iprot):
        if (
            iprot._fast_decode is not None
            and isinstance(iprot.trans, TTransport.CReadableTransport)
            and self.thrift_spec is not None
        ):
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 0:
                if ftype == TType.BOOL:
                    self.success = iprot.readBool()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin("is_healthy_result")
        if self.success is not None:
            oprot.writeFieldBegin("success", TType.BOOL, 0)
            oprot.writeBool(self.success)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ["%s=%r" % (key, getattr(self, key)) for key in self.__slots__]
        return "%s(%s)" % (self.__class__.__name__, ", ".join(L))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        for attr in self.__slots__:
            my_val = getattr(self, attr)
            other_val = getattr(other, attr)
            if my_val != other_val:
                return False
        return True

    def __ne__(self, other):
        return not (self == other)


all_structs.append(is_healthy_result)
is_healthy_result.thrift_spec = ((0, TType.BOOL, "success", None, None,),)  # 0
fix_spec(all_structs)
del all_structs

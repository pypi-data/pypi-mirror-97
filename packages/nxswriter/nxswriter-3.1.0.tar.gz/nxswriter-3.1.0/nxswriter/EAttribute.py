#!/usr/bin/env python
#   This file is part of nexdatas - Tango Server for NeXus data writer
#
#    Copyright (C) 2012-2017 DESY, Jan Kotanski <jkotan@mail.desy.de>
#
#    nexdatas is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    nexdatas is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with nexdatas.  If not, see <http://www.gnu.org/licenses/>.
#

""" Definitions of attribute tag evaluation classes """

import sys

import numpy

from .DataHolder import DataHolder
from .FElement import FElement


class EAttribute(FElement):

    """ attribute tag element
    """

    def __init__(self, attrs, last, streams=None):
        """ constructor

        :param attrs: dictionary of the tag attributes
        :type attrs: :obj:`dict` <:obj:`str`, :obj:`str`>
        :param last: the last element from the stack
        :type last: :class:`nxswriter.Element.Element`
        :param streams: tango-like steamset class
        :type streams: :class:`StreamSet` or :class:`PyTango.Device_4Impl`
        """

        FElement.__init__(self, "attribute", attrs, last, streams=streams)
        #: (:obj:`str`) attribute name
        self.name = ""
        #: (:obj:`str`) rank of the attribute
        self.rank = "0"
        #: (:obj:`dict` <:obj:`str`, :obj:`str`>) \
        #:         shape of the attribute, i.e. {index: length}
        self.lengths = {}
        #: (:obj:`str`) strategy, i.e. INIT, STEP, FINAL
        self.strategy = 'INIT'
        #: (:obj:`str`) trigger for asynchronous writting
        self.trigger = None

    def store(self, xml=None, globalJSON=None):
        """ stores the tag content

        :param xml: xml setting
        :type xml: :obj:`str`
        :param globalJSON: global JSON string
        :type globalJSON: \
        :     :obj:`dict` <:obj:`str`, :obj:`dict` <:obj:`str`, any>>
        :returns: (strategy,trigger)
        :rtype: (:obj:`str`, :obj:`str`)
        """

        if "name" in self._tagAttrs.keys():
            self.name = self._tagAttrs["name"]
            if "type" in self._tagAttrs.keys():
                tp = self._tagAttrs["type"]
            else:
                tp = "NX_CHAR"

            if tp == "NX_CHAR":
                shape = self._findShape(self.rank, self.lengths)
            else:
                shape = self._findShape(self.rank, self.lengths,
                                        extends=True, checkData=True)
            if sys.version_info > (3,):
                val = ("".join(self.content)).strip()
            else:
                val = ("".join(self.content)).strip().encode()
            if not shape:
                self.last.tagAttributes[self.name] = (tp, val)
            else:
                self.last.tagAttributes[self.name] = (tp, val, tuple(shape))

            if self.source:
                if self.source.isValid():
                    return self.strategy, self.trigger

    def run(self):
        """ runner

        :brief: During its thread run it fetches the data from the source
        """
        try:
            if self.name:
                if not self.h5Object:
                    #: stored H5 file object (defined in base class)
                    self.h5Object = self.last.h5Attribute(self.name)
                if self.source:
                    dt = self.source.getData()
                    dh = None
                    if dt:
                        dh = DataHolder(streams=self._streams, **dt)
                    if not dh:
                        message = self.setMessage("Data without value")
                        self.error = message
                    elif not hasattr(self.h5Object, 'shape'):
                        message = self.setMessage("PNI Object not created")
                        if self._streams:
                            self._streams.warn(
                                "Attribute::run() - %s " % message[0])
                        self.error = message
                    else:
                        self.h5Object[...] = dh.cast(self.h5Object.dtype)
        except Exception:
            message = self.setMessage(sys.exc_info()[1].__str__())
            self.error = message
        #            self.error = sys.exc_info()
        finally:
            if self.error:
                if self._streams:
                    if self.canfail:
                        self._streams.warn(
                            "Attribute::run() - %s  " % str(self.error))
                    else:
                        self._streams.error(
                            "Attribute::run() - %s  " % str(self.error))

    def __fillMax(self):
        """ fills object with maximum value

        :brief: It fills object or an extend part of object by default value

        """
        if self.name and not self.h5Object:
            self.h5Object = self.last.h5Attribute(self.name)
        shape = list(self.h5Object.shape)

        nptype = self.h5Object.dtype
        value = ''

        if nptype != "string":
            try:
                # workaround for bug #5618 in numpy for 1.8 < ver < 1.9.2
                #
                if nptype == 'uint64':
                    value = numpy.iinfo(getattr(numpy, 'int64')).max
                else:
                    value = numpy.iinfo(getattr(numpy, nptype)).max
            except Exception:
                try:
                    value = numpy.asscalar(
                        numpy.finfo(getattr(numpy, nptype)).max)
                except Exception:
                    value = 0
        else:
            nptype = "str"

        if shape and len(shape) > 0:
            arr = numpy.empty(shape, dtype=nptype)
            arr.fill(value)
        else:
            arr = value

        self.h5Object[...] = arr

    def markFailed(self, error=None):
        """ marks the field as failed

        :brief: It marks the field as failed
        :param error: error string
        :type error: :obj:`str`
        """
        field = self._lastObject()
        if field is not None:
            if error:
                if isinstance(error, tuple):
                    serror = str(tuple([str(e) for e in error]))
                else:
                    serror = str(error)
                if "nexdatas_canfail_error" in \
                   [at.name for at in field.attributes]:
                    olderror = field.attributes["nexdatas_canfail_error"][...]
                    if olderror:
                        serror = str(olderror) + "\n" + serror
                field.attributes.create("nexdatas_canfail_error", "string",
                                        overwrite=True)[...] = serror
            field.attributes.create("nexdatas_canfail", "string",
                                    overwrite=True)[...] = "FAILED"
            if self._streams:
                self._streams.info(
                    "EAttribute::markFailed() - "
                    "%s of %s marked as failed" %
                    (self.h5Object.name
                     if hasattr(self.h5Object, "name") else None,
                     field.name if hasattr(field, "name") else None))
            self.__fillMax()

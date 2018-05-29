#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tools for Pixelink PDS movies

@author: Nicolas Bruot (https://www.bruot.org/hp/)
@date: 29 May 2018
"""

import os
import numpy
import struct


class PdsReader(object):
    """Provides an interface to read a Pixelink PDS movie"""

    def __init__(self, path):
        self.path = path
        self._file_size = os.path.getsize(path)

        # Basic file size check
        if self._file_size < 8:
            raise ValueError('The file is not in PDS format (size less than 8 bytes).')
        self._f = open(path, 'rb')

        # Read movie dimensions
        self._f.seek(0)
        magic = self._f.read(4)
        if magic != b'\x04\x04\x04\x04':
            raise ValueError('The file is not in PDS format (wrong magic sequence).')
        self.n_frames = struct.unpack('I', self._f.read(4))[0]
        self._f.seek(0x1b4)
        self.width = int(struct.unpack('<f', self._f.read(4))[0])
        self.height = int(struct.unpack('<f', self._f.read(4))[0])
        self._f.seek(0x1c8)
        pixel_fmt = struct.unpack('<f', self._f.read(4))[0]
        if pixel_fmt == 0.0:
            self.bytes_per_sample = 1
        elif pixel_fmt == 1.0:
            self.bytes_per_sample = 2
        else:
            raise ValueError('Unknown pixel format.')

        # Second file size check, knowing now the frame size
        if self._file_size != 8 + (584 + self._frame_size()) * self.n_frames:
            raise ValueError('Wrong file size.')


    def _frame_size(self):
        """Returns the size in bytes of a frame"""

        return self.width * self.height * self.bytes_per_sample


    def data(self, frame=None):
        """Returns pixel data of the movie

        If `frame` is not specified, the data for the whole movie is returned
        as a 3d NumPy array. If `frame` is specified, it returns the 2d data
        for the given frame.
        """

        if self.n_frames == 0:
            return numpy.zeros((0, 0, 0))

        frame_size = self._frame_size()
        data_type = '>u%d' % self.bytes_per_sample
        if frame is not None:
            self._f.seek(0x8 + (584 + self._frame_size()) * frame + 584)
            data = numpy.empty((self.height, self.width),
                           dtype=data_type)
            lin_frame_data = numpy.frombuffer(self._f.read(frame_size),
                                              data_type)
            return lin_frame_data.reshape((self.height, self.width))
        else:
            data = numpy.empty((self.n_frames, self.height, self.width),
                               dtype=data_type)
            self._f.seek(0x8)
            for i in range(self.n_frames):
                self._f.seek(584, 1)
                lin_frame_data = numpy.frombuffer(self._f.read(frame_size),
                                                  data_type)
                data[i] = lin_frame_data.reshape((self.height, self.width))
            return data


    def timestamps(self, frame=None):
        """Returns frames' timestamps

        If `frame` is given, the timestamp of the specified frame is returned,
        otherwise the method returns an array of all timestamps.
        """

        if frame is not None:
            self._f.seek(0x8 +  (584 + self._frame_size()) * frame + 0x4)
            return struct.unpack('<f', self._f.read(4))[0]
        else:
            self._f.seek(0x8 + 0x4)
            timestamps = numpy.empty((self.n_frames, ), dtype='<f4')
            frame_size = self._frame_size()
            for i in range(self.n_frames):
                timestamps[i] = struct.unpack('<f', self._f.read(4))[0]
                self._f.seek(580 + frame_size, 1)
            return timestamps


__all__ = ['PdsReader']

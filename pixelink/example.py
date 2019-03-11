#!/usr/bin/env python
# -*- coding: utf-8 -*-


# This file is part of the python-pixelink software.
#
# Copyright 2018-2019 Nicolas Bruot and CNRS (https://www.bruot.org/hp/)
#
#
# python-pixelink is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# python-pixelink is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with python-pixelink.  If not, see <http://www.gnu.org/licenses/>.


"""Example showing how to use python-pixelink"""


from matplotlib import pyplot as plt
import numpy as np
import pixelink


path = '/path/to/your/movie.pds'

pds = pixelink.PdsReader(path)

print('Number of frames: %d' % pds.n_frames)
print('Frame width: %d' % pds.width)
print('Frame height: %d' % pds.height)

print('Timestamp of the first frame (s): %f' % pds.timestamps(0))

# Timestamps of all frames:
timestamps = pds.timestamps()
plt.figure()
plt.plot(timestamps)
plt.xlabel('Frame')
plt.ylabel('Time (s)')
plt.title('Timestamps')
plt.show()

# Pixel data of first frame
i = 0
data0 = pds.data(i)
plt.figure()
plt.imshow(data0)
plt.xlabel('x')
plt.ylabel('y')
plt.title('Frame %d' % i)
plt.show()

# Pixel data of all frames
data = pds.data()
# Check that the first frame in the 3d `data` array matches `data0`
print('data0 == data[0]? %s' % np.array_equal(data0, data[0]))
# Time evolution of pixel (20, 30)
x = 20
y = 30
plt.figure()
plt.plot(timestamps, data[:, x, y])
plt.xlabel('Time (s)')
plt.ylabel('Pixel value')
plt.title('Pixel (%d, %d)' % (x, y))
plt.show()

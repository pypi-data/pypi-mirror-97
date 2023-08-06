===============================================
 `xotless.ranges`:mod: -- Continuous intervals
===============================================

.. module:: xotless.ranges

.. testsetup:: *

   from xotless.ranges import *


.. autoclass:: Range
   :members: new_open, new_closed, new_open_left, new_open_right, sample,
             kind, lift, empty, __bool__, __contains__, bound, diff, join,
             __and__, __eq__, __le__, __lt__, __ge__, __gt__


.. autoclass:: Included
   :members: safer_new

.. autoclass:: Excluded

.. autoclass:: RangeKind

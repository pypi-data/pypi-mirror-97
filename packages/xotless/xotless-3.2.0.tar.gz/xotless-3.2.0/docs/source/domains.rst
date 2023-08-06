=========================================
 `xotless.domains`:mod: -- Value domains
=========================================

.. module:: xotless.domains

.. testsetup::

   from xotless.domains import *

Domains are used by AVMs to describe values of an attribute for which a
program behaves in the same way.

Domains behave as sets containing elements of a single type.  They all support
the functions of the `Domain`:class: type:

.. autoclass:: Domain
   :members: sample, union, __sub__, __and__, __contains__, __le__, __lt__,
             __ge__, __gt__


There are two implementations of domains.

.. class:: EquivalenceSet

   Wraps a Python-set in the API of domains.  It cannot represent infinite
   domains.

   Non-empty equivalence sets always produce a `~Domain.sample`:attr:.

   .. automethod:: to_interval_set


.. class:: IntervalSet

   A domain represented by several continuous `ranges
   <xotless.ranges.Range>`:class:.


.. autofunction:: iter_domain_endpoints(domains: Sequence[Domain[T]]) -> Iterator[T]

=========
 History
=========

Releases 3.x
============

2021-03-07.  Release 3.2.0
--------------------------

- Add `xotless.domains.iter_domain_endpoints`:func:.


2020-11-11.  Release 3.1.0
--------------------------

- Fix issue `#3`__: `xotless.trees.IntervalTree`:class: didn't allow boundless
  cells.

  A couple of project use IntervalTree with None to represent `±Infinity
  <xotl.tools.infinity.Infinity>`:any: boundaries.

  Furthermore, `~xotless.trees.Cell.from_range`:meth: would set the Infinity
  boundaries in previous versions:

     >>> from xotless.trees import Cell
     >>> from xotless.ranges import Range
     >>> Cell.from_range(Range.new_open(None, None), 1)
     Cell(lowerbound=-Infinity, upperbound=Infinity, data=1)

  With this change, now `~xotless.trees.Cell.from_bounds`:meth: behaves
  equivalently:

     >>> Cell.from_bounds(None, None, 1)
     Cell(lowerbound=-Infinity, upperbound=Infinity, data=1)


__ https://gitlab.merchise.org/mercurio-2018/xotless/-/issues/3


2020-11-02.  Release 3.0.0
--------------------------

- Update to hypothesis 5.26+.

  Due to Hypothesis' issue `2537
  <https://github.com/HypothesisWorks/hypothesis/issues/2537>`__, this
  introduces a minor breaking change.


Releases 2.x
============


2020-10-30.  Release 2.1.0
--------------------------

- Implement ``__bool__`` for `xotless.immutable.ImmutableWrapper`:class:.


2020-07-24.  Release 2.0.0
--------------------------

- Require 'xotl.tools' instead of 'xoutil'.  This is a breaking change because
  applications must switch all their packages that require 'xoutil' to
  'xotl.tools'


First releases 1.x
==================

2020-07-22.  Release 1.8.1
--------------------------

- Continued from `#2`__: Ensure all datetimes produced in our strategies are
  unfolded.

  Since we're using timezone unaware datetime, is not actually meaningful
  ``fold``.

__ https://gitlab.merchise.org/mercurio-2018/xotless/-/issues/2


2020-07-22.  Release 1.8.0
--------------------------

- Deprecate `xotless.pickablenv`:mod:.

- Make `xotless.immutables.ImmutableWrapper`:class: participate in the
  ``__getitem__`` protocol.

- Fixed `#2`__: Use newer versions of `hypothesis`_ in tests.

__ https://gitlab.merchise.org/mercurio-2018/xotless/-/issues/2

.. _hypothesis: https://hypothesis.readthedocs.io/


2020-07-01.  Release 1.7.0
--------------------------

- Fix `xotless.pickablenv.EnvironmentData`:class: to ensure the found
  environment is in the list of ``odoo.api.Environment``.

  In certain cases (installing uninstalling addons) the environment in the
  request is being discarded and you need to get the new environments.


2020-07-01.  Release 1.6.0
--------------------------

- Fix a bug with `xotless.pickablenv.PickableRecordset.from_recordset`:meth:
  which cached the Odoo instance.  We should not cache Odoo instances since
  version `1.4.0 <release-1.4.0>`:ref:.


2020-06-24.  Release 1.5.0
--------------------------

- Make the hash of an ImmutableWrapper without overrides be the same as the
  underlying object.

.. _release-1.4.0:

2020-06-05.  Release 1.4.0
--------------------------

- Don't cache Odoo instances in `xotless.pickablenv.PickableRecordset`:class:,
  but also prefer the current HTTP Odoo Environment to avoid looking for an
  arbitrary one.

  This solves a `couple <xhg2#979>`_ of `bugs <xhg2#939>`_ in Mercurio 2018

  .. _xhg2#979: https://gitlab.merchise.org/mercurio-2018/xhg2/-/issues/979
  .. _xhg2#939: https://gitlab.merchise.org/mercurio-2018/xhg2/-/issues/939


2020-05-26.  Release 1.3.0
--------------------------

- Add module `xotless.walk`:mod:.


2020-05-19.  Release 1.2.0
--------------------------

- `xotless.immutables.ImmutableWrapper`:class: now accepts argument
  `wraps_descriptors` to apply wrapper on while invoking descriptors.


2020-04-30.  Release 1.1.0
--------------------------

- Use ``__slots__`` in `xotless.trees.IntervalTree`:class:.  We don't expect
  instances of this class to need additional attributes.


2020-04-29.  Release 1.0.1
--------------------------

This release only contains packaging fixes to make the distribution compliant
with PEP :pep:`561`.


2020-04-29.  Release 1.0.0
--------------------------

The first release including the code extracted from a bigger project.  Modules
available are `xotless.ranges`:mod:, `xotless.trees`:mod:,
`xotless.domains`:mod:, `xotless.itertools`:mod:, `xotless.immutables`:mod:,
and `xotless.pickablenv`:mod:.

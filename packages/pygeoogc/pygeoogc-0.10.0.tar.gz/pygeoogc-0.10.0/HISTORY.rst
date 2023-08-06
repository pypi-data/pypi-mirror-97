=======
History
=======

0.10.0 (unreleased)
-------------------

- The first release after renaming hydrodata to pygeohydro.
- Fix ``extent`` property of ``ArcGISRESTful`` being set to ``None`` incorrectly.
- Add ``feature types`` property to ``ArcGISRESTFul`` for getting names and IDs of types
  of features in the database.
- Replace ``cElementTree`` with ``ElementTree`` since it's been deprecated by ``defusedxml``.
- Remove dependency on ``dataclasses`` since its benefits and usage in the code was minimal.
- Speed up CI testing by using ``mamba`` and caching.

0.9.0 (2021-02-14)
------------------

- Bump version to the same version as pygeohydro.
- Add support for query by point and multi-points to ``ArcGISRESTful.bygeom``.
- Add support for buffer distance to ``ArcGISRESTful.bygeom``.
- Add support for generating ESRI-based queries for points and multi-points
  to ``ESRIGeomQuery``.
- Add all the missing type annotations.
- Update the Daymet url to version 4. You can check the release information
  `here <https://daac.ornl.gov/DAYMET/guides/Daymet_Daily_V4.html>`_
- Use ``cytoolz`` library for some of the operations for improving performance.
- Add ``extent`` property to ``ArcGISRESTful`` class that get the spatial extent
  of the service.
- Add url to ``airmap`` service for getting elevation data at 30 m resolution.

0.2.3 (2020-12-19)
-------------------

- Fix ``urlib3`` deprecation warning about using ``method_whitelist``.

0.2.2 (2020-12-05)
-------------------

- Remove unused variables in ``async_requests`` and use ``max_workers``.
- Fix the ``async_requests`` issue on Windows systems.


0.2.0 (2020-12-06)
-------------------

- Added/Renamed three class methods in ``ArcGISRESTful``: ``oids_bygeom``, ``oids_byfield``,
  and ``oids_bysql``. So you can query feature within a geometry, using specific field ID(s),
  or more generally using any valid SQL 92 WHERE clause.
- Added support for query with SQL WHERE clause to ``ArcGISRESTful``.
- Changed the NLDI's URL for migrating to its new API v3.
- Added support for CQL filter to ``WFS``, credits to `Emilio <https://github.com/emiliom>`__.
- Moved all the web services URLs to a YAML file that ``ServiceURL`` class reads. It makes
  managing the new URLs easier. The file is located at ``pygeoogc/static/urls.yml``.
- Turned off threading by default for all the services since not all web services supports it.
- Added support for setting the request method, ``GET`` or ``POST``, for ``WFS.byfilter``,
  which could be useful when the filter string is long.
- Added support for asynchronous download via the function ``async_requests``.


0.1.10 (2020-08-18)
-------------------

- Improved ``bbox_decompose`` to fix the ``WMS`` issue with high resolution requests.
- Replaces ``simplejson`` with ``orjson`` to speed up json operations.

0.1.8 (2020-08-12)
------------------

- Removed threading for ``WMS`` due to inconsistent behavior.
- Addressed an issue with domain decomposition for ``WMS`` where width/height becomes 0.

0.1.7 (2020-08-11)
------------------

- Renamed ``vsplit_bbox`` to ``bbox_decompose``. The function now decomposes the domain
  in both directions and return squares and rectangular.

0.1.5 (2020-07-23)
------------------

- Re-wrote ``wms_bybox`` function as a class called ``WMS`` with a similar
  interface to the ``WFS`` class.
- Added support for WMS 1.3.0 and WFS 2.0.0.
- Added a custom ``Exception`` for the threading function called ``ThreadingException``.
- Add ``always_xy`` flag to ``WMS`` and ``WFS`` which is False by default. It is useful
  for cases where a web service doesn't change the axis order from the transitional
  ``xy`` to ``yx`` for versions higher than 1.3.0.

0.1.3 (2020-07-21)
------------------

- Remove unnecessary transformation of the input bbox in WFS.
- Use ``setuptools_scm`` for versioning.

0.1.2 (2020-07-16)
------------------

- Add the missing ``max_pixel`` argument to the ``wms_bybox`` function.
- Change the ``onlyIPv4`` method of ``RetrySession`` class to ``onlyipv4``
  to conform to the ``snake_case`` convention.
- Improve docstrings.

0.1.1 (2020-07-15)
------------------

- Initial release.

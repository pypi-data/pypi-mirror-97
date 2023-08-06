# Copyright (c) 2013-2015 Siphon Contributors.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
"""Test NCSS access code."""

from contextlib import contextmanager
from datetime import datetime

import numpy as np

from siphon.ncss import NCSS, NCSSQuery, ResponseRegistry
import siphon.testing

recorder = siphon.testing.get_recorder(__file__)


def test_ncss_query_proj_box():
    """Test forming a query with a projected bounding box."""
    nq = NCSSQuery().lonlat_point(1, 2).projection_box(-1, -2, -3, -4)
    query = str(nq)
    assert query.count('=') == 4
    assert 'minx=-1' in query
    assert 'maxx=-3' in query
    assert 'miny=-2' in query
    assert 'maxy=-4' in query


def test_ncss_query_vertical_level():
    """Test making a query with a vertical level."""
    nq = NCSSQuery().vertical_level(50000)
    assert str(nq) == 'vertCoord=50000'


def test_ncss_query_add_latlon():
    """Test query when requesting adding lon and lat."""
    nq = NCSSQuery().add_lonlat(True)
    assert str(nq) == 'addLatLon=True'


def test_ncss_query_strides():
    """Test making a query with strides."""
    nq = NCSSQuery().strides(5, 10)
    query = str(nq)
    assert 'timeStride=5' in query
    assert 'horizStride=10' in query


def test_ncss_query_accept():
    """Test making a query with an accept."""
    nq = NCSSQuery().accept('csv')
    assert str(nq) == 'accept=csv'


@contextmanager
def response_context():
    """Override the response handler registry for testing.

    This way we can force unhandled cases.
    """
    old_reg = siphon.ncss.response_handlers
    siphon.ncss.response_handlers = ResponseRegistry()
    yield siphon.ncss.response_handlers
    siphon.ncss.response_handlers = old_reg


# For testing unit handling
def tuple_unit_handler(data, units=None):
    """Return data as a list, with units as necessary."""
    return np.array(data).tolist(), units


class TestNCSS(object):
    """Test NCSS queries and response parsing."""

    server = 'http://thredds.ucar.edu/thredds/ncss/'
    url_path = 'grib/NCEP/GFS/Global_0p5deg/GFS_Global_0p5deg_20150612_1200.grib2'

    @recorder.use_cassette('ncss_test_metadata')
    def setup(self):
        """Set up for tests with a default valid query."""
        dt = datetime(2015, 6, 12, 15, 0, 0)
        self.ncss = NCSS(self.server + self.url_path)
        self.nq = self.ncss.query().lonlat_point(-105, 40).time(dt)
        self.nq.variables('Temperature_isobaric', 'Relative_humidity_isobaric')

    def test_good_query(self):
        """Test that a good query is properly validated."""
        assert self.ncss.validate_query(self.nq)

    def test_bad_query(self):
        """Test that a query with an unknown variable is invalid."""
        self.nq.variables('foo')
        assert not self.ncss.validate_query(self.nq)

    def test_empty_query(self):
        """Test that an empty query is invalid."""
        query = self.ncss.query()
        res = self.ncss.validate_query(query)
        assert not res
        assert not isinstance(res, set)

    def test_bad_query_no_vars(self):
        """Test that a query without variables is invalid."""
        self.nq.var.clear()
        assert not self.ncss.validate_query(self.nq)

    @recorder.use_cassette('ncss_gfs_xml_point')
    def test_xml_point(self):
        """Test parsing XML point returns."""
        self.nq.accept('xml')
        xml_data = self.ncss.get_data(self.nq)

        assert 'Temperature_isobaric' in xml_data
        assert 'Relative_humidity_isobaric' in xml_data
        assert xml_data['lat'][0] == 40
        assert xml_data['lon'][0] == -105

    @recorder.use_cassette('ncss_gfs_csv_point')
    def test_csv_point(self):
        """Test parsing CSV point returns."""
        self.nq.accept('csv')
        csv_data = self.ncss.get_data(self.nq)

        assert 'Temperature_isobaric' in csv_data
        assert 'Relative_humidity_isobaric' in csv_data
        assert csv_data['lat'][0] == 40
        assert csv_data['lon'][0] == -105

    @recorder.use_cassette('ncss_gfs_csv_point')
    def test_unit_handler_csv(self):
        """Test unit-handling from CSV returns."""
        self.nq.accept('csv')
        self.ncss.unit_handler = tuple_unit_handler
        csv_data = self.ncss.get_data(self.nq)

        temp = csv_data['Temperature_isobaric']
        assert len(temp) == 2
        assert temp[1] == 'K'

        relh = csv_data['Relative_humidity_isobaric']
        assert len(relh) == 2
        assert relh[1] == '%'

    @recorder.use_cassette('ncss_gfs_xml_point')
    def test_unit_handler_xml(self):
        """Test unit-handling from XML returns."""
        self.nq.accept('xml')
        self.ncss.unit_handler = tuple_unit_handler
        xml_data = self.ncss.get_data(self.nq)

        temp = xml_data['Temperature_isobaric']
        assert len(temp) == 2
        assert temp[1] == 'K'

        relh = xml_data['Relative_humidity_isobaric']
        assert len(relh) == 2
        assert relh[1] == '%'

    @recorder.use_cassette('ncss_gfs_netcdf_point')
    def test_netcdf_point(self):
        """Test handling of netCDF point returns."""
        self.nq.accept('netcdf')
        nc = self.ncss.get_data(self.nq)

        assert 'Temperature_isobaric' in nc.variables
        assert 'Relative_humidity_isobaric' in nc.variables
        assert nc.variables['latitude'][0] == 40
        assert nc.variables['longitude'][0] == -105

    @recorder.use_cassette('ncss_gfs_netcdf4_point')
    def test_netcdf4_point(self):
        """Test handling of netCDF4 point returns."""
        self.nq.accept('netcdf4')
        nc = self.ncss.get_data(self.nq)

        assert 'Temperature_isobaric' in nc.variables
        assert 'Relative_humidity_isobaric' in nc.variables
        assert nc.variables['latitude'][0] == 40
        assert nc.variables['longitude'][0] == -105

    @recorder.use_cassette('ncss_gfs_vertical_level')
    def test_vertical_level(self):
        """Test data return from a single vertical level is correct."""
        self.nq.accept('csv').vertical_level(50000)
        csv_data = self.ncss.get_data(self.nq)

        np.testing.assert_almost_equal(csv_data['Temperature_isobaric'], np.array([263.40]), 2)

    @recorder.use_cassette('ncss_gfs_csv_point')
    def test_raw_csv(self):
        """Test CSV point return from a GFS request."""
        self.nq.accept('csv')
        csv_data = self.ncss.get_data_raw(self.nq)

        assert csv_data.startswith(b'date,lat')

    @recorder.use_cassette('ncss_gfs_csv_point')
    def test_unknown_mime(self):
        """Test handling of unknown mimetypes."""
        self.nq.accept('csv')
        with response_context():
            csv_data = self.ncss.get_data(self.nq)
            assert csv_data.startswith(b'date,lat')

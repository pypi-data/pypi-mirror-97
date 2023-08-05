# -*- coding: utf-8 -*-
#  Copyright (c) 2020. Distributed under the terms of the MIT License.

from pathlib import Path

import numpy as np
import pytest
from pymatgen.electronic_structure.core import Spin

from vise.analyzer.band_edge_properties import (
    BandEdge, BandEdgeProperties, is_band_gap)
from vise.defaults import defaults
from vise.tests.helpers.assertion import assert_msonable

parent_dir = Path(__file__).parent


actual_kpt = [[10.1, 10.2, 10.3], [10.4, 10.5, 10.6]]
expected_metal = \
    {'energies': 0.0, 'direct': None, 'transition': None}, None, None


def test_band_edge_msonable():
    assert_msonable(BandEdge(energy=0.0, spin=Spin.up, band_index=0,
                             kpoint_index=1, kpoint_coords=[0.0, 0.0, 0.0]))


def test_band_edge_equal():
    e1 = BandEdge(0.0, Spin.up,   band_index=0, kpoint_coords=[0.0, 0.0, 0.0])
    e2 = BandEdge(0.0, Spin.up,   band_index=0, kpoint_coords=[0.0, 0.0, 0.0])
    e3 = BandEdge(0.0, Spin.up,   band_index=0, kpoint_coords=[0.1, 0.0, 0.0])
    e4 = BandEdge(0.0, Spin.down, band_index=0, kpoint_coords=[0.0, 0.0, 0.0])
    assert e1.is_direct(e2) is True
    assert e1.is_direct(e3) is False
    assert e1.is_direct(e4) is False


def test_metal_judged_from_non_uniform_band_occupation():
    eigenvalues = {Spin.up: np.array([[0.0, 0.1, 0.2], [0.2, 0.3, 0.4]])}
    band_edge = BandEdgeProperties(eigenvalues=eigenvalues,
                                   nelect=4.0,
                                   magnetization=0.0,
                                   kpoints=actual_kpt)

    assert band_edge.band_gap is None
    assert band_edge.is_direct is None
    assert band_edge.vbm_info is None
    assert band_edge.cbm_info is None


def test_metal_judged_from_fractional_nelect():
    eigenvalues = {Spin.up: np.array([[0.0, 1.0, 2.0], [0.1, 1.1, 2.1]])}
    integer_criterion = 0.1
    band_edge = BandEdgeProperties(eigenvalues=eigenvalues,
                                   nelect=4.0 + integer_criterion + 1e-5,
                                   magnetization=0.0,
                                   kpoints=actual_kpt,
                                   integer_criterion=0.1)

    assert band_edge.band_gap is None
    assert band_edge.is_direct is None
    assert band_edge.vbm_info is None
    assert band_edge.cbm_info is None


def test_metal_judged_from_fractional_magnetization():
    eigenvalues = {Spin.up:   np.array([[0.0, 1.0, 10.0], [0.0, 1.1, 10.0]]),
                   Spin.down: np.array([[0.0, 1.4, 10.0], [0.0, 1.5, 10.0]])}
    integer_criterion = 0.1
    band_edge = BandEdgeProperties(eigenvalues=eigenvalues,
                                   nelect=3.0,
                                   magnetization=1.0 + integer_criterion + 1e-5,
                                   kpoints=actual_kpt,
                                   integer_criterion=0.1)

    assert band_edge.band_gap is None
    assert band_edge.is_direct is None
    assert band_edge.vbm_info is None
    assert band_edge.cbm_info is None


def test_nonmagnetic_insulator():
    # k-point indices run fast.
    eigenvalues = {Spin.up: np.array([[0.0, 1.0, 2.0], [0.1, 1.1, 2.1]])}
    integer_criterion = 0.1
    band_edge = BandEdgeProperties(eigenvalues=eigenvalues,
                                   nelect=4.0 + integer_criterion - 1e-5,
                                   magnetization=0.0,
                                   kpoints=actual_kpt,
                                   integer_criterion=0.1)

    assert pytest.approx(band_edge.band_gap) == 0.90

    assert band_edge.is_direct is False

    assert pytest.approx(band_edge.vbm_info.energy) == 1.1
    assert pytest.approx(band_edge.cbm_info.energy) == 2.0

    assert band_edge.vbm_info.spin == Spin.up
    assert band_edge.cbm_info.spin == Spin.up

    assert band_edge.vbm_info.band_index == 1
    assert band_edge.cbm_info.band_index == 2

    assert band_edge.vbm_info.kpoint_coords == [10.4, 10.5, 10.6]
    assert band_edge.cbm_info.kpoint_coords == [10.1, 10.2, 10.3]


@pytest.fixture
def band_edge():
    eigenvalues = {Spin.up:   np.array([[0.0, 1.0, 10.0], [0.0, 1.1, 10.0]]),
                   Spin.down: np.array([[0.0, 1.4, 10.0], [0.0, 1.5, 10.0]])}
    return BandEdgeProperties(eigenvalues=eigenvalues,
                              nelect=3.0,
                              magnetization=1.0,
                              kpoints=actual_kpt)


def test_magnetic_insulator(band_edge):

    assert pytest.approx(band_edge.band_gap) == 0.3

    assert band_edge.is_direct is False

    assert pytest.approx(band_edge.vbm_info.energy) == 1.1
    assert pytest.approx(band_edge.cbm_info.energy) == 1.4

    assert band_edge.vbm_info.spin == Spin.up
    assert band_edge.cbm_info.spin == Spin.down

    assert band_edge.vbm_info.band_index == 1
    assert band_edge.cbm_info.band_index == 1

    assert band_edge.vbm_info.kpoint_coords == [10.4, 10.5, 10.6]
    assert band_edge.cbm_info.kpoint_coords == [10.1, 10.2, 10.3]


def test_is_metal():
    band_edge_metal = BandEdgeProperties(
        eigenvalues={Spin.up: np.array([[0, 1, 2], [0, 3, 4]])},
        nelect=4.0,
        magnetization=0.0,
        kpoints=actual_kpt)
    assert band_edge_metal.is_metal is True
    assert band_edge_metal.vbm_info is None
    assert band_edge_metal.cbm_info is None
    assert band_edge_metal.vbm_cbm is None
    assert band_edge_metal.band_gap is None
    assert repr(band_edge_metal) == "Metal"


def test_repr(band_edge):
    expected = """Band gap 0.300 eV
VBM energy position: 1.1, spin:   up, band index 1, k-point index 1, k-point coords 10.400 10.500 10.600
CBM energy position: 1.4, spin: down, band index 1, k-point index 0, k-point coords 10.100 10.200 10.300"""
    assert repr(band_edge) == expected


def test_is_band_gap():
    assert is_band_gap(None, [1.0, 1.0 + defaults.band_gap_criterion + 1e-5]) is True
    assert is_band_gap(None, [1.0, 1.0 + defaults.band_gap_criterion - 1e-5]) is False
    assert is_band_gap(None, None) is False

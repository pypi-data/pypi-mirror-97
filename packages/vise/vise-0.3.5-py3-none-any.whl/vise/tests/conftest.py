# -*- coding: utf-8 -*-
import json
from pathlib import Path

import pytest
from pymatgen.core import Lattice
from pymatgen.core.structure import Structure


@pytest.fixture(scope="session")
def test_data_files():
    return Path(__file__).parent / "test_data_files"


@pytest.fixture(scope="session")
def sc_structure():
    lattice = Lattice.cubic(1.0)
    coords = [[0.0, 0.0, 0.0]]
    return Structure(lattice=lattice, species=["H"], coords=coords)


@pytest.fixture(scope="session")
def mc_structure():
    lattice =[[ 6.0, 3.0, 0.0],
              [ 6.0,-3.0, 0.0],
              [-4.0, 0.0, 7.0]]
    coords = [[0.0, 0.0, 0.0]]
    return Structure(lattice=lattice, species=["H"], coords=coords)


@pytest.fixture(scope="session")
def complex_monoclinic_structure():
    coords = [[0.0, 0.0, 0.0],
              [0.1, 0.0, 0.0],
              [0.9, 0.0, 0.0],
              [0.2, 0.0, 0.0],
              [0.8, 0.0, 0.0],
              ]
    return Structure(lattice=Lattice.monoclinic(10, 20, 30, 75),
                     species=["H", "He", "He", "He", "He"],
                     coords=coords)



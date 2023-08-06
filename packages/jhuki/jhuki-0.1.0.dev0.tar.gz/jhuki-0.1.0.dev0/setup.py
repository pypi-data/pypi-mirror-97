# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jhuki', 'jhuki.externals', 'jhuki.externals.nrpypn']

package_data = \
{'': ['*']}

install_requires = \
['ConfigArgParse>=1.2.3,<2.0.0', 'sympy>=1.7.1,<2.0.0']

setup_kwargs = {
    'name': 'jhuki',
    'version': '0.1.0.dev0',
    'description': 'Utilities to prepare Einstein Toolkit simulations',
    'long_description': '<p align="center">\n<img src="https://github.com/Sbozzolo/jhuki/raw/master/logo.png" height="250">\n</p>\n\n[![GPLv3\nlicense](https://img.shields.io/badge/License-GPLv3-blue.svg)](http://perso.crans.org/besson/LICENSE.html)\n![Tests](https://github.com/Sbozzolo/Jhuki/workflows/Tests/badge.svg)\n\n\nWriting parameter files for Cactus simulations is not easy. To achieve a\nsuccessful evolution, one has to tune several parameters, which typically depend\non the grid configuration or on other settings. Writing these par files by hand\nis tedious and error-prone. `Jhuki` is a Python library to prepare\nsimulations for the `Einstein Toolkit` (or Cactus-based codes).\n\n> :warning: This package is currently under development. It may be full of bugs,\n>           and its interfaces might change without notice.\n\n## Features\n\n* Generate parameter files from a template using configuration files or\n  command-line arguments\n* Take care of the grid configuration given the desired resolution at the finest\n  level and other details\n\n## Examples\n\n### Working with grid structures\n\nProblem: you want to generate the parfile code for a grid structure with two\nrefinement centers, each with 8 levels and resolution at the finest level 0.001\nand CFL factor of 0.4 (in the finest level). In this, you want to ensure that\nthe maximum timestep on the grid never exceeds 1 to avoid numerical instability.\n\n``` python\n#!/usr/bin/env python3\n\nfrom jhuki import grid as pg\n\nrefinement_radii = tuple(2**level for level in range(7))\n\ncenter1 = pg.RefinementCenter(refinement_radii,\n                              dx_fine=0.001,\n                              cfl_fine=0.5,\n                              center_num=1,\n                              position=(10,0,0))\n\n# Same but with different center_num and position\ncenter2 = pg.RefinementCenter(refinement_radii,\n                              dx_fine=0.001,\n                              cfl_fine=0.5,\n                              center_num=2,\n                              position=(-10,0,0))\n\ngrid_not_synced = pg.Grid((center1, center2), outer_boundary=1000)\ngrid_synced = pg.set_dt_max_grid(grid_not_synced, dt_max=1)\n\nprint(grid_synced.parfile_code)\n```\nThis will output\n\n``` sh\nCartGrid3D::type = "coordbase"\nCarpet::domain_from_coordbase = "yes"\nCoordBase::domainsize = "minmax"\nCoordBase::xmin = 1000\nCoordBase::ymin = 1000\nCoordBase::zmin = 1000\nCoordBase::xmax = 1000\nCoordBase::ymax = 1000\nCoordBase::zmax = 1000\nCoordBase::dx = 0.64\nCoordBase::dy = 0.64\nCoordBase::dz = 0.64\nCarpet::max_refinement_levels = 8\nCarpet::time_refinement_factors = "[1,1,2,4,8,16,32,64]"\nCarpetRegrid2::num_levels_1 = 8\nCarpetRegrid2::position_x_1 = 10\nCarpetRegrid2::position_y_1 = 0\nCarpetRegrid2::position_z_1 = 0\nCarpetRegrid2::radius_1[1] = 64\nCarpetRegrid2::radius_1[2] = 32\nCarpetRegrid2::radius_1[3] = 16\nCarpetRegrid2::radius_1[4] = 8\nCarpetRegrid2::radius_1[5] = 4\nCarpetRegrid2::radius_1[6] = 2\nCarpetRegrid2::radius_1[7] = 1\nCarpetRegrid2::num_levels_2 = 8\nCarpetRegrid2::position_x_2 = -10\nCarpetRegrid2::position_y_2 = 0\nCarpetRegrid2::position_z_2 = 0\nCarpetRegrid2::radius_2[1] = 64\nCarpetRegrid2::radius_2[2] = 32\nCarpetRegrid2::radius_2[3] = 16\nCarpetRegrid2::radius_2[4] = 8\nCarpetRegrid2::radius_2[5] = 4\nCarpetRegrid2::radius_2[6] = 2\nCarpetRegrid2::radius_2[7] = 1\n```\n\nYou can also add a small shift to the grid so that the origin is not on (0,0,0)\npassing the `tiny_shift` argument to `Grid`.\n\n## Installation\n\nThe best way to install `Jhuki` is by cloning this repo and using\n[poetry](https://python-poetry.org/). If you have poetry install, just run\n`poetry install` in the folder where you cloned the repo to install `Jhuki`.\n\n## Tests\n\n`Jhuki` comes with a suite of unit tests. To run the tests,\n```sh\npoetry run pytest --cov=./ --cov-report=term\n```\nTests are automatically run after each commit by GitHub Actions. This will also\ntell you what is the test coverage.\n\n# Code style\n\n- We lint the code with `black -l 79`.\n\n# What does _jhuki_ mean?\n\nThe word _jhuki_ belongs to the Tohono O\'odham vocabulary and means *rain*. If\n[kuibit](https://githum.com/Sbozzolo/kuibit) is the tool you use to collect the\nfruit of your `Cactus` simulations, then `jhuki` is what allowed that fruit to\nbe there in the first place.\n\n## Credits\n\nThe logo contains elements designed by [pngtree.com](pngtree.com).\n\nThe computation of the momenta for quasi-circular mergers of binary black holes\nuses\n[NRPyPN](https://einsteintoolkit.org/thornguide/EinsteinInitialData/NRPyPN/documentation.html).\nIf you use this module, please follow the citation guidelines as specified by\nthe documentation in the `NRPyPN` repo.\n',
    'author': 'Gabriele Bozzola',
    'author_email': 'gabrielebozzola@arizona.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sbozzolo/Jhuki',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

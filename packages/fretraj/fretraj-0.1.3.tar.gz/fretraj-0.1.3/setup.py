# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['fretraj']

package_data = \
{'': ['*'], 'fretraj': ['UI/*', 'examples/*']}

install_requires = \
['PyQt5>=5.12.3,<6.0.0',
 'mdtraj>=1.9.5,<2.0.0',
 'numba<=0.50.1',
 'numpy<1.20.0',
 'packaging>=20.9,<21.0',
 'pandas>=1.2.2,<2.0.0']

entry_points = \
{'console_scripts': ['fretraj = fretraj.cloud:main',
                     'fretraj_gui = fretraj.gui:main',
                     'pymol_vis = skripts.console:pymol_vis',
                     'vmd_vis = skripts.console:vmd_vis']}

setup_kwargs = {
    'name': 'fretraj',
    'version': '0.1.3',
    'description': 'Predicting FRET with accessible-contact volumes',
    'long_description': '# <img src="docs/images/fretraj_logo.png" width="200">\n[![Build Status](https://github.com/fdsteffen/fretraj/workflows/FRETraj%20build/badge.svg)](https://github.com/fdsteffen/fretraj/actions)\n[![Docs Status](https://github.com/fdsteffen/fretraj/workflows/FRETraj%20docs/badge.svg)](https://github.com/fdsteffen/fretraj/actions)\n[![codecov](https://codecov.io/gh/fdsteffen/fretraj/branch/master/graph/badge.svg?token=A2E70FbycQ)](https://codecov.io/gh/fdsteffen/fretraj)\n\n*FRETraj* is a Python module for calculating **multiple accessible-contact volumes** (multi-ACV) and predicting **FRET efficiencies**. It provides an interface to the [*LabelLib*](https://github.com/Fluorescence-Tools/LabelLib) library to simulate fluorophore dynamics. The package features a user-friendly **PyMOL plugin**<sup>[1](#pymol)</sup> which can be used to explore different labeling positions when designing FRET experiments. In an AV simulation the fluorophore distribution is estimated by a shortest path search (Djikstra algorithm) using a coarse-grained dye probe. *FRETraj* further implements a **Python-only** version of the geometrical clash search used in *LabelLib*. This should facilitate prototyping of new features for the ACV algorithm.\n\n<img src="docs/images/graphical_abstract.png">\n     \nA recent addition to the original AV model (Kalinin et al. *Nat. Methods*, 2012) is the so-called **contact volume** (Steffen et. al. *PCCP* 2016). Here, the accessible volume is split into a free volume (FV, transparent) where the dye is freely diffusing and a contact volume (CV, opaque) where the dye stacks to the biomolecular surface. Time-resolved anisotropy experiments suggest that certain fluorophores, among those the commonly used cyanine fluorophores Cy3 and Cy5, are particularly prone to interact with both proteins and nucleic acids. The contact volume accounts for this effect by reweighting the point-cloud. By choosing different experimental weights for the free and contact component the AV dye model is refined, making *in silico* FRET predictions more reliable.\n\n## Installation\nFollow the instructions for your platform [here](https://fdsteffen.github.io/fretraj/getting_started/installation)\n\n## References\nIf you use **FRETraj** in your work please refer to the following paper:\n- F.D. Steffen, R.K.O. Sigel, R. Börner, *Phys. Chem. Chem. Phys.* **2016**, *18*, 29045-29055. [![](https://img.shields.io/badge/DOI-10.1039/C6CP04277E-blue.svg)](https://doi.org/10.1039/C6CP04277E)\n\nHere, we introduce the contact volume (CV) as an extension of the accessible volume (AV).\n\n### Related projects\nThe accessible volume is described in:\n- S. Kalinin, T. Peulen, C.A.M. Seidel et al. *Nat. Methods*, **2012**, *9*, 1218-1225. [![](https://img.shields.io/badge/DOI-10.1038/nmeth.2222-blue.svg)](https://doi.org/10.1038/nmeth.2222)\n\nFast-NPS (nano-positioning system) uses a Bayesian model to locate a dye with respect to a biomolecule: \n- T. Eilert, M. Beckers, F. Drechsler, J. Michaelis, *Comput. Phys. Commun.*, **2017**, *219*, 377–389. [![](https://img.shields.io/badge/DOI-10.1016/j.cpc.2017.05.027-blue.svg)](https://doi.org/10.1016/j.cpc.2017.05.027)\n\nVarious dye models have been reviewed in:\n- M. Dimura, T. Peulen, C.A.M. Seidel et al. *Curr. Opin. Struct. Biol.* **2016**, *40*, 163-185. [![](https://img.shields.io/badge/DOI-10.1016/j.sbi.2016.11.012-blue.svg)](https://doi.org/10.1016/j.sbi.2016.11.012)\n- T. Peulen, O. Opanasyuk, C.A.M Seidel, *J. Phys. Chem . B.*, **2017**, *121*, 8211-8241.[![](https://img.shields.io/badge/DOI-10.1021/acs.jpcb.7b03441-blue.svg)](https://doi.org/10.1021/acs.jpcb.7b03441)\n\nA recent benchmark for FRET-assisted modeling of proteins is described in:\n- M. Dimura, T. Peulen, C.A.M Seidel et al. *Nat. Commun.* **2020**, *11*, 5394.\n[![](https://img.shields.io/badge/DOI-10.1038/s41467--020--19023--1-blue.svg)](https://doi.org/10.1038/s41467-020-19023-1)\n\n---\n\n<sup><a name="pymol">1</a></sup> PyMOL is a trademark of Schrödinger, LLC.\n',
    'author': 'Fabio Steffen',
    'author_email': 'fabio.steffen@chem.uzh.ch',
    'maintainer': 'Fabio Steffen',
    'maintainer_email': 'fabio.steffen@chem.uzh.ch',
    'url': 'https://rna-fretools.github.io/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<3.9',
}


setup(**setup_kwargs)

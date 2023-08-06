# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['evfuncs']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.18.1', 'scipy>=1.2.0']

setup_kwargs = {
    'name': 'evfuncs',
    'version': '0.3.2.post1',
    'description': 'Functions for working with files created by the EvTAF program and the evsonganaly GUI',
    'long_description': '[![Build Status](https://github.com/NickleDave/evfuncs/actions/workflows/ci.yml/badge.svg)\n[![DOI](https://zenodo.org/badge/158776329.svg)](https://zenodo.org/badge/latestdoi/158776329)\n[![PyPI version](https://badge.fury.io/py/evfuncs.svg)](https://badge.fury.io/py/evfuncs)\n[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)\n# *ev*funcs\nFunctions for working with files created by EvTAF and the evsonganaly GUI.  \nIn case you need to work with those files in Python 😊😊😊 (see "Usage" below).\n\nThe first work published with data collected using EvTAF and evsonganaly is in this paper:  \nTumer, Evren C., and Michael S. Brainard.  \n"Performance variability enables adaptive plasticity of ‘crystallized’adult birdsong."  \nNature 450.7173 (2007): 1240.  \n<https://www.nature.com/articles/nature06390>  \n\nThese functions are translations to Python of the original functions \nwritten in MATLAB (copyright Mathworks) by Evren Tumer (shown below).  \n<p style="text-align:center;">\n<img src="./doc/ev_ev_ev.png" alt="Image of Evren">\n</p>\n\n### Installation\n`$ pip install evfuncs`\n\n### Usage\n\nThe main purpose for developing these functions in Python was to \nwork with files of Bengalese finch song in this data repository: \n<https://figshare.com/articles/Bengalese_Finch_song_repository/4805749>\n\nUsing `evfuncs` with that repository, you can load the `.cbin` audio files ...\n```Python\n>>> import evfuncs\n\n>>> rawsong, samp_freq = evfuncs.load_cbin(\'gy6or6_baseline_230312_0808.138.cbin\')\n```\n\n... and the annotation in the `.not.mat` files ...\n```Python\n>>> notmat_dict = evfuncs.load_notmat(\'gy6or6_baseline_230312_0808.138.cbin\')\n```\n(or, using the `.not.mat` filename directly)\n```Python\n>>> notmat_dict = evfuncs.load_notmat(\'gy6or6_baseline_230312_0808.138.not.mat\')\n```\n\n...and you should be able to reproduce the segmentation of the raw audio files of birdsong\ninto syllables and silent periods, using the segmenting parameters from a .not.mat file and \nthe simple algorithm applied by the SegmentNotes.m function.\n\n```Python\n>>> smooth = evfuncs.smooth_data(rawsong, samp_freq)\n>>> threshold = notmat_dict[\'threshold\']\n>>> min_syl_dur = notmat_dict[\'min_dur\'] / 1000\n>>> min_silent_dur = notmat_dict[\'min_int\'] / 1000\n>>> onsets, offsets = evfuncs.segment_song(smooth, samp_freq, threshold, min_syl_dur, min_silent_dur)\n>>> import numpy as np\n>>> np.allclose(onsets, notmat_dict[\'onsets\'])\nTrue\n```\n(*Note that this test would return `False` if the onsets and offsets in the .not.mat \nannotation file had been modified, e.g., a user of the evsonganaly GUI had edited them,\nafter they were originally computed by the SegmentNotes.m function.*)\n\n`evfuncs` is used to load annotations by  \n[\'crowsetta\'](https://github.com/NickleDave/crowsetta), \na data-munging tool for building datasets of vocalizations \nthat can be used to train machine learning models.\nTwo machine learning libraries that can use those datasets are: \n[`hybrid-vocal-classifier`](https://hybrid-vocal-classifier.readthedocs.io/en/latest/), \nand [`vak`](https://github.com/NickleDave/vak).\n\n### Getting Help\nPlease feel free to raise an issue here:  \nhttps://github.com/NickleDave/evfuncs/issues\n\n### License\n[BSD License](./LICENSE).\n\n### Citation\nIf you use this package, please cite the DOI:  \n[![DOI](https://zenodo.org/badge/158776329.svg)](https://zenodo.org/badge/latestdoi/158776329)\n\n### Build Status\n[![Build Status](https://travis-ci.com/NickleDave/evfuncs.svg?branch=master)](https://travis-ci.com/NickleDave/evfuncs)\n',
    'author': 'David Nicholson',
    'author_email': 'nickledave@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/NickleDave/evfuncs',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)

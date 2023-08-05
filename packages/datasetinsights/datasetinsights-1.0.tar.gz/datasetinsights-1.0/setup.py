# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datasetinsights',
 'datasetinsights.commands',
 'datasetinsights.datasets',
 'datasetinsights.datasets.unity_perception',
 'datasetinsights.io',
 'datasetinsights.io.downloader',
 'datasetinsights.stats',
 'datasetinsights.stats.visualization']

package_data = \
{'': ['*'], 'datasetinsights.stats.visualization': ['font/*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'codetiming>=1.2.0,<2.0.0',
 'cython>=0.29.14,<0.30.0',
 'dash==1.12.0',
 'dask[complete]>=2.14.0,<3.0.0',
 'google-cloud-storage>=1.24.1,<=1.28.1',
 'jupyter>=1.0.0,<2.0.0',
 'matplotlib>=3.3.1,<4.0.0',
 'numpy>=1.17,<1.18',
 'opencv-python>=4.4.0.42,<5.0.0.0',
 'pandas>=1.0.1,<2.0.0',
 'plotly>=4.4.1,<5.0.0',
 'pyquaternion>=0.9.5,<0.10.0',
 'tqdm>=4.45.0,<5.0.0']

entry_points = \
{'console_scripts': ['datasetinsights = datasetinsights.__main__:entrypoint']}

setup_kwargs = {
    'name': 'datasetinsights',
    'version': '1.0',
    'description': 'Synthetic dataset insights.',
    'long_description': "# Dataset Insights\n\nUnity Dataset Insights is a python package for downloading, parsing and analyzing synthetic datasets generated using the Unity [Perception package](https://github.com/Unity-Technologies/com.unity.perception).\n\n## Installation\n\nDataset Insights maintains a pip package for easy installation. It can work in any standard Python environment using `pip install datasetinsights` command. We support Python 3 (3.7 and 3.8).\n\n## Getting Started\n\n### Dataset Statistics\n\nWe provide a sample [notebook](notebooks/Perception_Statistics.ipynb) to help you load synthetic datasets generated using [Perception package](https://github.com/Unity-Technologies/com.unity.perception) and visualize dataset statistics. We plan to support other sample Unity projects in the future.\n\n### Dataset Download\n\nYou can download the datasets from HTTP(s), GCS, and Unity simulation projects using the 'download' command from CLI or API.\n\n[CLI](https://datasetinsights.readthedocs.io/en/latest/datasetinsights.commands.html#datasetinsights-commands-download)\n\n```bash\ndatasetinsights download \\\n  --source-uri=<xxx> \\\n  --output=$HOME/data\n```\n[Programmatically](https://datasetinsights.readthedocs.io/en/latest/datasetinsights.io.downloader.html#module-datasetinsights.io.downloader.gcs_downloader)\n\n```python3\n\nfrom datasetinsights.io.downloader import UnitySimulationDownloader,\nGCSDatasetDownloader, HTTPDatasetDownloader\n\ndownloader = UnitySimulationDownloader(access_token=access_token)\ndownloader.download(source_uri=source_uri, output=data_root)\n\ndownloader = GCSDatasetDownloader()\ndownloader.download(source_uri=source_uri, output=data_root)\n\ndownloader = HTTPDatasetDownloader()\ndownloader.download(source_uri=source_uri, output=data_root)\n\n```\n\n## Docker\n\nYou can use the pre-build docker image [unitytechnologies/datasetinsights](https://hub.docker.com/r/unitytechnologies/datasetinsights) to run similar commands.\n\n## Documentation\n\nYou can find the API documentation on [readthedocs](https://datasetinsights.readthedocs.io/en/latest/).\n\n## Contributing\n\nPlease let us know if you encounter a bug by filing an issue. To learn more about making a contribution to Dataset Insights, please see our Contribution [page](CONTRIBUTING.md).\n\n## License\n\nDataset Insights is licensed under the Apache License, Version 2.0. See [LICENSE](LICENCE) for the full license text.\n\n## Citation\nIf you find this package useful, consider citing it using:\n```\n@misc{datasetinsights2020,\n    title={Unity {D}ataset {I}nsights Package},\n    author={{Unity Technologies}},\n    howpublished={\\url{https://github.com/Unity-Technologies/datasetinsights}},\n    year={2020}\n}\n```\n",
    'author': 'Unity AI Perception Team',
    'author_email': 'computer-vision@unity3d.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://datasetinsights.readthedocs.io/en/latest/Evaluation_Tutorial.html',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['datapane',
 'datapane.client',
 'datapane.client.api',
 'datapane.client.api.report',
 'datapane.client.scripts',
 'datapane.common',
 'datapane.resources',
 'datapane.resources.local_report',
 'datapane.resources.report_def',
 'datapane.resources.templates',
 'datapane.resources.templates.report_py',
 'datapane.resources.templates.script',
 'datapane.runner']

package_data = \
{'': ['*'], 'datapane.resources.templates': ['report_ipynb/*']}

install_requires = \
['PyYAML>=5.3.0,<6.0.0',
 'altair>=4.0.0,<5.0.0',
 'bleach>=3.2.1,<4.0.0',
 'bokeh>=2.2.0,<3.0.0',
 'boltons>=20.2.1,<21.0.0',
 'click-spinner>=0.1.8,<0.2.0',
 'click>=7.0.0,<8.0.0',
 'colorlog>=4.1.0,<5.0.0',
 'dacite>=1.5.0,<2.0.0',
 'dominate>=2.4.0,<3.0.0',
 'flit-core>=3.0.0,<3.1.0',
 'folium>=0.12.0,<0.13.0',
 'furl>=2.1.0,<3.0.0',
 'glom>=20.11.0,<21.0.0',
 'importlib_resources>=5.0.0,<6.0.0',
 'jinja2>=2.11.1,<3.0.0',
 'jsonschema>=3.2.0,<4.0.0',
 'lxml>=4.5.2,<5.0.0',
 'matplotlib>=3.1.0,<4.0.0',
 'micawber>=0.5.2,<0.6.0',
 'munch>=2.5.0,<3.0.0',
 'nbconvert>=6.0.0,<6.1.0',
 'numpy>=1.18.0,<2.0.0',
 'packaging>=20.3,<21.0',
 'pandas>=1.0.1,<2.0.0',
 'plotly>=4.8.1,<5.0.0',
 'pyarrow>=3.0.0,<4.0.0',
 'requests-toolbelt>=0.9.1,<0.10.0',
 'requests>=2.20.0,<3.0.0',
 'ruamel.yaml>=0.16.5,<0.17.0',
 'stringcase>=1.2.0,<2.0.0',
 'tabulate>=0.8.7,<0.9.0',
 'toolz>=0.11.1,<0.12.0',
 'validators>=0.18.0,<0.19.0']

extras_require = \
{':python_version >= "3.6.1" and python_version < "3.7.0"': ['dataclasses==0.7']}

entry_points = \
{'console_scripts': ['datapane = datapane.client.__main__:main',
                     'dp-runner = datapane.runner.__main__:main']}

setup_kwargs = {
    'name': 'datapane',
    'version': '0.10.2',
    'description': 'Datapane client library and CLI tool',
    'long_description': '<p align="center">\n  <a href="https://datapane.com">\n    <img src="https://datapane.com/static/datapane-logo-dark.png" width="250px" alt="Datapane" />\n  </a>\n</p>\n<p align="center">\n    <a href="https://datapane.com">Datapane.com</a> |\n    <a href="https://docs.datapane.com">Documentation</a> |\n    <a href="https://twitter.com/datapaneapp">Twitter</a> |\n    <a href="https://datapane.com/enterprise">Enterprise</a>\n    <br /><br />\n    <a href="https://pypi.org/project/datapane/">\n        <img src="https://img.shields.io/pypi/dm/datapane?label=pip%20downloads" alt="Pip Downloads" />\n    </a>\n    <a href="https://pypi.org/project/datapane/">\n        <img src="https://img.shields.io/pypi/v/datapane?color=blue" alt="Latest release" />\n    </a>\n    <a href="https://anaconda.org/conda-forge/datapane">\n        <img alt="Conda (channel only)" src="https://img.shields.io/conda/vn/conda-forge/datapane">\n    </a>\n</p>\n\nDatapane is a Python library which makes it simple to build reports from the common objects in your data analysis, such as pandas DataFrames, plots from Python visualisation libraries, and Markdown.\n\nReports can be exported as standalone HTML documents, with rich components which allow data to be explored and visualisations to be used interactively.\n\nFor example, if you wanted to create a report with a table viewer and an interactive plot:\n\n```python\nimport pandas as pd\nimport altair as alt\nimport datapane as dp\n\ndf = pd.read_csv(\'https://query1.finance.yahoo.com/v7/finance/download/GOOG?period2=1585222905&interval=1mo&events=history\')\n\nchart = alt.Chart(df).encode(\n    x=\'Date:T\',\n    y=\'Open\'\n).mark_line().interactive()\n\nr = dp.Report(dp.DataTable(df), dp.Plot(chart))\nr.save(path=\'report.html\', open=True)\n```\n\nThis would package a standalone HTML report such as the following, with a searchable DataTable and Plot component.\n\n![Report Example](https://i.imgur.com/RGp7RzM.png)\n\n# Getting Started\n\n## Install\n\n- `pip3 install datapane` OR\n- `conda install -c conda-forge "datapane>=0.10.0"`\n\n## Next Steps\n\n- [Read the documentation](https://docs.datapane.com)\n- [Browse samples and demos](https://github.com/datapane/datapane-demos/)\n- [View featured reports](https://datapane.com/explore/?tab=featured)\n\n# Datapane Public\n\nIn addition to saving reports locally, [Datapane](datapane.com) provides a free hosted platform at https://datapane.com where you to publish your reports online.\n\nPublished reports can be:\n\n- shared publicly and become a part of our community,\n- embedded within your blogs, CMSs, and elsewhere (see [here](https://docs.datapane.com/reports/embedding-reports-in-social-platforms)),\n- shared private reports you can share within a close-knit audience,\n- include explorations and integrations, e.g. additional DataTable analysis features and [GitHub action](https://github.com/datapane/build-action) integration.\n\nIt\'s super simple, just login (see [here](https://docs.datapane.com/tut-getting-started#authentication)) and call the `publish` function on your report,\n\n```python\nr = dp.Report(dp.DataTable(df), dp.Plot(chart))\nr.publish(name="2020 Stock Portfolio", open=True)\n```\n\n# Enterprise\n\n[Datapane Enterprise](https://datapane.com/enterprise/) provides automation and secure sharing of reports within in your organization.\n\n- Private report sharing within your organization and within groups, including external clients\n- Deploy Notebooks and scripts as automated, parameterised reports that can be run by your team interactively\n- Schedule reports to be generated and shared\n- Runs managed or on-prem\n- [and more](<(https://datapane.com/enterprise/)>)\n\n# Joining the community\n\nLooking to get answers to questions or engage with us and the wider community? Check out our [GitHub Discussions](https://github.com/datapane/datapane/discussions) board.\n\nSubmit requests, issues, and bug reports on this GitHub repo.\n\nWe look forward to building an amazing open source community with you!\n',
    'author': 'Datapane Team',
    'author_email': 'dev@datapane.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.datapane.com',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)

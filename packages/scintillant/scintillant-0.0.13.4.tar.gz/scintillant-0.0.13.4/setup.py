from setuptools import setup
from scintillant import about

# load the README file and use it as the long_description for PyPI
with open('README.md', 'r') as f:
    readme = f.read()

# package configuration - for reference see:
# https://setuptools.readthedocs.io/en/latest/setuptools.html#id9
setup(
    name=about['__title__'],
    description=about['__description__'],
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    version=about['__version__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    url=about['__url__'],
    packages=[
        'scintillant',
        'scintillant.apimodels',
        'scintillant.apimodels.models',
        'scintillant.apimodels.db',
        'scintillant.controllers',
        'scintillant.commands',
        'scintillant.outs'
    ],
    include_package_data=True,
    python_requires=">=3.8.*",
    install_requires=['tqdm', 'requests', 'livereload', 'Click'],
    license=about['__license__'],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'scintillant = scintillant.entry_points:main',
            'snlt = scintillant.entry_points:main'
        ],
    },
    keywords='package development template'
)

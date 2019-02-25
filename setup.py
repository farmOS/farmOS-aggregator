import io

from setuptools import find_packages, setup

with io.open('README.md', 'rt', encoding='utf8') as f:
    readme = f.read()

setup(
    name='farmOSaggregator',
    version='1.0.0',
    url='https://github.com/farmOS/farmOS-aggregator',
    license='GPLv3',
    maintainer='Michael Stenta',
    maintainer_email='mike@mstenta.net',
    description='An application for aggregating data from multiple farmOS instances.',
    long_description=readme,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'flask-admin',
        'flask-sqlalchemy',
        'sqlalchemy',
    ],
)

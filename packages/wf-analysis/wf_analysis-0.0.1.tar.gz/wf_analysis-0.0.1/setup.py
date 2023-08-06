#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Install script for package"""

from distutils.core import setup

setup(
    name='wf_analysis',  # How you named your package folder (MyLib)
    packages=['wf_analysis'],  # Chose the same as "name"
    version='0.0.1',  # Start with a small number and increase it with every change you make
    license='GPL',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description='Utilities and libraries for waveform reconstruction comparisons and residuals analysis',
    # Give a short description about your library
    author='Sudarshan Ghonge',  # Type in your name
    author_email='sudarshan.ghonge@ligo.org',  # Type in your E-Mail
    url='https://git.ligo.org/sudarshan-ghonge/wf-analysis',
    # Provide either the link to your github or to your website
    download_url='https://git.ligo.org/sudarshan-ghonge/wf-analysis/-/archive/master/wf-analysis-master.tar.gz',
    # I explain this later on
    keywords=['burst', 'cbc', 'reconstruction', 'residuals', 'waveforms'],  # Keywords that define your package best
    install_requires=['astropy>=2.0.3', 'atomicwrites', 'attrs==20.3.0',
                      'backports.functools-lru-cache==1.6.1', 'beautifulsoup4==4.9.0',
                      'certifi==2020.12.5', 'chardet==3.0.4', 'corner==2.0.1',
                      'cycler==0.10.0', 'decorator==4.4.2', 'emcee==2.2.1',
                      'funcsigs==1.0.2', 'gwpy==2.0.2', 'h5py==2.10.0', 'idna==2.10',
                      'Jinja2==2.11.2', 'kiwisolver==1.3.1', 'kombine==0.8.4',
                      'lalsuite==6.82', 'linecache2==1.0.0', 'lscsoft-glue==2.0.0',
                      'Mako==1.1.4', 'MarkupSafe==1.1.1', 'matplotlib~=3.3.4',
                      'more-itertools==4.2.0', 'mpld3==0.3', 'numpy~=1.20.1',
                      'pandas>0.25.3', 'pesummary~=0.11.0', 'Pillow==8.1.1',
                      'pluggy==0.13.0', 'py==1.8.1', 'PyCBC==1.18.0',
                      'pyparsing==2.4.7', 'pyRXP==2.1.0',
                      'pytest==5.3.5', 'python-dateutil==2.8.1', 'pytz==2021.1',
                      'requests==2.23.0', 'scipy~=1.6.1', 'six==1.14.0',
                      'subprocess32==3.5.2', 'traceback2==1.4.0', 'unittest2==1.1.0',
                      'urllib3==1.25.8'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',  # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)',  # Again, pick a license
        'Programming Language :: Python :: 3.7',  # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.8',

    ],
)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Install script for package"""
from distutils.core import setup

setup(
    name='bayeswave_pipe',  # How you named your package folder (MyLib)
    packages=['bayeswave_pipe'],  # Chose the same as "name"
    version='0.0.0',  # Start with a small number and increase it with every change you make
    license='GPL',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description='Scripts and packages for bayeswave, reconstruction comparisons and residuals analysis workflows.',
    # Give a short description about your library
    author='Sudarshan Ghonge',  # Type in your name
    author_email='sudarshan.ghonge@ligo.org',  # Type in your E-Mail
    url='https://git.ligo.org/sudarshan-ghonge/bayeswave_pipe',
    # Provide either the link to your github or to your website
    download_url='',
    # I explain this later on
    keywords=['condor', 'dags', 'bayeswave', 'wf-analysis'],  # Keywords that define your package best
    install_requires=['ligo_segments==1.2.0', 'lscsoft_glue==2.0.0',
                      'numpy==1.19.2', 'pandas==1.1.3', 'pesummary~=0.11.0'],
    scripts=['scripts/bayeswave_pipe', 'scripts/gwcomp_pipe'],

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

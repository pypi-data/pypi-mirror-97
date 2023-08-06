#!/usr/bin/env python

import sys
from setuptools import setup

def main():
    project_name = 'STT'
    if '--project_name' in sys.argv:
        project_name_idx = sys.argv.index('--project_name')
        project_name = sys.argv[project_name_idx + 1]
        sys.argv.remove('--project_name')
        sys.argv.pop(project_name_idx)

    setup(
        name=project_name,
        version='0.10.0-alpha.4',
        description='A library for doing speech recognition using a Coqui STT model',
        long_description='Full project description and documentation on `https://stt.readthedocs.io/ <https://stt.readthedocs.io/>`_',
        long_description_content_type='text/x-rst; charset=UTF-8',
        author='Coqui GmbH',
        packages=['stt'],
        license='MPL-2.0',
        url='https://github.com/coqui-ai/STT',
        project_urls={
            'Documentation': 'https://stt.readthedocs.io',
            'Tracker': 'https://github.com/coqui-ai/STT/issues',
            'Repository': 'https://github.com/coqui-ai/STT',
            'Discussions': 'https://github.com/coqui-ai/STT/discussions',
        },
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Topic :: Multimedia :: Sound/Audio :: Speech',
            'Topic :: Scientific/Engineering :: Human Machine Interfaces',
            'Topic :: Scientific/Engineering',
            'Topic :: Utilities',
        ],
    )

if __name__ == '__main__':
    main()

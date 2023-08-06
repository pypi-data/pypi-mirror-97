from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='tom-registration',
    version='0.1.0a1',
    description='Reusable TOMToolkit app to support multiple user registration flows',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/TOMToolkit/tom_registration',
    author='TOM Toolkit Project',
    author_email='dcollom@lco.global',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering :: Astronomy',
        'Topic :: Scientific/Engineering :: Physics'
    ],
    keywords=['tomtoolkit', 'astronomy', 'astrophysics', 'cosmology', 'science', 'fits', 'observatory'],
    packages=find_packages(),
    # use_scm_version={'version_scheme': 'no-guess-dev'},
    setup_requires=['setuptools_scm', 'wheel'],
    install_requires=[
        'tomtoolkit>=2.6.0'
    ],
    extras_require={
        'test': ['factory_boy==3.2.0']
    },
    include_package_data=True,
)

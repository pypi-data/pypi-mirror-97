import sys
import os

try:
    from setuptools import setup, Extension
    from setuptools.command.build_ext import build_ext as _build_ext
except ImportError:
    from distutils.core import setup, Extension
    from distutils.command.build_ext import build_ext as _build_ext

import re

doc_files = [r'C:\dafne\SimpleElastix\LICENSE',r'C:\dafne\SimpleElastix\NOTICE',r'C:\dafne\SimpleElastix\README.md',r'C:\dafne\SimpleElastix\build\SimpleITK-build\ITK-5.1-NOTICE',r'C:\dafne\SimpleElastix\build\SimpleITK-build\ITK-5.1-README.md']

def get_pep386version():
    """This method examines the SimpleITK's CMake version variables to make a pep 386 compliant version string when building a version indented for distribution."""
    sitkMAJOR = "2"
    sitkMINOR = "0"
    sitkPATCH = "0"
    sitkTWEAK = ""
    sitkRC    = "rc2"
    sitkPOST  = ""
    sitkDEV   = "908"
    sitkHASH  = "8244e"


    version = sitkMAJOR+"."+sitkMINOR

    if sitkPATCH:
        version += "."+sitkPATCH
        if sitkTWEAK:
            version += "."+sitkTWEAK

    if  sitkRC:
        version += sitkRC

    if sitkPOST:
        version += ".post"+sitkPOST
    elif sitkDEV:
        version += ".dev"+sitkDEV

    # Local Version Identifier
    #if sitkHASH and not "OFF" in ['1', 'ON']:
    #    version += "+g"+sitkHASH

    return version

class build_ext(_build_ext):
    """ Override standard command class to build an extension, to
    simply copy an existing compiled library into the packaging
    directory structure.
    """

    def build_extension(self, ext):
        """
        """
        from distutils.errors import DistutilsSetupError

        sources = ext.sources
        if sources is None or not len(sources) == 1:
            raise DistutilsSetupError( "Expected only one compiled library." )

        expected_ext_filename = os.path.split(self.get_ext_filename(ext.name))[1]

        ext_file = self.get_ext_fullpath(ext.name)

        abs_sources = list( map(os.path.abspath, sources) )

        self.copy_file(abs_sources[0], ext_file)


setup(
    name = 'SimpleITK-SimpleElastix',
    version = get_pep386version(),
    author = 'Insight Software Consortium',
    author_email = 'insight-users@itk.org',
    ext_modules=[Extension('SimpleITK._SimpleITK', [r'_SimpleITK.pyd'])],
    packages= ['SimpleITK'],
    package_dir = {'SimpleITK':r'C:\dafne\SimpleElastix\build\SimpleITK-build\Wrapping\Python'},
    data_files = [("", doc_files)],
    download_url = r'https://www.itk.org/SimpleITKDoxygen/html/PyDownloadPage.html',
    platforms = [],
    description = r'SimpleITK is a simplified interface to the Insight Toolkit (ITK) for image registration and segmentation',
    long_description  = 'SimpleITK provides an abstraction layer to ITK that enables developers \
                         and users to access the powerful features of the InsightToolkit in an easy \
                         to use manner for biomedical image analysis.',
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: C++",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Education",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: MacOS"
        ],
    license='Apache',
    keywords = 'SimpleITK ITK InsightToolkit segmentation registration',
    url = r'http://simpleitk.org/',
    cmdclass={'build_ext':build_ext}
)

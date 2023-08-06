from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="dsp-metadata-gui",
    version="0.0.0-rc6",
    description="Python GUI tool to collect metadata for DSP projects.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dasch-swiss/dsp-metadata-gui",
    author="Balduin Landolt",
    author_email="balduin.landolt@dasch.swiss",
    license="GPLv3",
    packages=["dspMetadataGUI", "dspMetadataGUI.util"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9.0",
    install_requires=[
        "decorator==4.4.2",
        "isodate==0.6.0",
        "numpy==1.20.1; python_version >= '3.0'",
        "owlrl==5.2.1",
        "pillow==8.1.0; python_version >= '3.6'",
        "pyparsing==2.4.7; python_version >= '2.6' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "pyshacl==0.14.2",
        "rdflib==5.0.0",
        "rdflib-jsonld==0.5.0",
        "six==1.15.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "validators==0.18.2",
        "wxpython==4.1.1",
    ],
    entry_points={
        "console_scripts": [
            "dsp-metadata=dspMetadataGUI.collectMetadata:collectMetadata"
        ],
    },
    include_package_data=True,
    zip_safe=False,
)

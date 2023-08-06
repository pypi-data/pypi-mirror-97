import setuptools
import pp_cedp

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name=pp_cedp.__name__,
    version=pp_cedp.__version__,
    author=pp_cedp.__author__,
    author_email=pp_cedp.__author_email__,
    description="Privacy-Preserving Continuous Event Data Publishing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/m4jidRafiei/PP_CEDP",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'pylcs==0.0.6',
        'pandas>=0.24.2',
        'numpy>=1.18.2',
        'pm4py==1.2.10'
    ],
    project_urls={
        'Source': 'https://github.com/m4jidRafiei/PP_CEDP'
    }
)


import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="EcMasterPython",
    version="3.1.1.02",
    author="acontis technologies GmbH",
    author_email="ecsupport@acontis.com",
    description="The Python Wrapper provides a Python interface to use EC-Master and RAS Client/Server for EtherCAT.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org/acontis",
    project_urls={
        "Website": "https://www.acontis.com/",
        "Programming Interface": "https://public.acontis.com/manuals/EC-Master/3.1/html/ec-master-python/index.html",
    },
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Cython",
        "Programming Language :: C",
        "Programming Language :: C++",
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Unix",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Networking",
    ],
    keywords="EtherCAT EC-Master Acontis Library",
    packages=setuptools.find_packages(),    
    python_requires=">=3.6",
    include_package_data=True,
    license="proprietary and confidential",
    package_data= {
        "EcMasterPython": [
          "Examples/EcMasterDemoPython/*.*",
          "Sources/EcWrapperPython/*.*",
        ],
    },
)
import setuptools

setuptools.setup(
    name='metricserverremote',
    version='1.7',
    url='http://www.opalesystems.com',
    license='MIT',
    author='Adnane BERRADA',
    author_email='support@opalesystems.com',
    install_requires=[
        'zeep',
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    description='Opale MetricServer remote Python API'
)

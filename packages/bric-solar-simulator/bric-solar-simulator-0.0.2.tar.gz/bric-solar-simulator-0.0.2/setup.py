import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bric-solar-simulator",
    version="0.0.2",
    author="Brian Carlsen",
    author_email="carlsen.bri@gmail.com",
    description="Control and interface for Arduino driven, LED solar simulator.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha"
    ],
    install_requires=[
        'bric_arduino_controllers'
    ],
    package_data={
        'driver_documentation': [ '8_Channel_LED_driver-documentation.docx' ]
    }
)
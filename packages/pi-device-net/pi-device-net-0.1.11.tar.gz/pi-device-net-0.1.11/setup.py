import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pi-device-net",
    version="0.1.11",
    author="Edwin Wise",
    author_email="edwin@simreal.com",
    description="A set of tools to operate a device network.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EdwinWiseOne/PiDeviceNet",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: Free for non-commercial use",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Home Automation",
        "Topic :: Software Development :: Libraries",
    ],
    python_requires='>=3.7',
    install_requires=['paho-mqtt', 'pygame'],
)
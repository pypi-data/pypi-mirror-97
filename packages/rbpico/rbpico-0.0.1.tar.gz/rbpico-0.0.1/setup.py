import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rbpico", # Replace with your own username
    version="0.0.1",
    author="Neil Lambeth",
    author_email="neil@redrobotics.co.uk",
    description="Python Library to control a RedBoard+ via I2C using a Raspberry Pi PICO as an I2C secondary device.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RedRobotics/RBPico",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
)

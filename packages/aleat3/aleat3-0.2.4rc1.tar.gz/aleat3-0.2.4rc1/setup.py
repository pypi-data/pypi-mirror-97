import setuptools

#from setuptools.config import read_configuration
#conf_dict = read_configuration("C:/Program Files/Ramz Editions/Packaaging Examples/Aleatoryous 3/0.2/setup.cfg")

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aleat3",
    version="0.2.4rc1",
    author="Diego Ramirez",
    author_email="dr01191115@gmail.com",
    description="An aleatory syntaxes package. Third generation.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Customer Service",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Operating System :: MacOS",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Microsoft :: Windows :: Windows 7",
        "Operating System :: Microsoft :: Windows :: Windows 8",
        "Operating System :: Unix",
        "Topic :: Games/Entertainment",
        "Topic :: Software Development"
    ],
    keywords="aleatory dice coin roulette python aleat",
    python_requires='>=3.6, <4',
    entry_points={
        "console_scripts": [
            "aleat3=aleat3.console.console_main",
            "aleat3_demo=aleat3.main:demo",
            "aleat3_coin=aleat3.main:coin",
            "aleat3_dice=aleat3.main:dice",
            "aleat3_roulette=aleat3.main:roulette"
        ]
    },
    install_requires=["pip>=20.0"] # Attempt to update the pip after instaling aleat3.
)

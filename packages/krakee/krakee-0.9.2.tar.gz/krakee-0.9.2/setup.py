from setuptools import setup, find_packages

setup(
    name="krakee",
    version="0.9.2",
    author="Ruben Afonso",
    author_email="rbfrancos@gmail.com",
    description="Kraken Exchange API with a thin pandas Dataframe wrap",
    url="https://github.com/rubenafo/krakee",
    keywords = ["kraken", "cryptocurrencies", "exchange", "python", "bitcoin", "trading", "crypto"],
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires = ['krakenex', 'pandas', 'pykrakenapi']
)

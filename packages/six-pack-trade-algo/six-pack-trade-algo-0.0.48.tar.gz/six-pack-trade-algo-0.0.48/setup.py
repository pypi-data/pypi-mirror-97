import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="six-pack-trade-algo", # Replace with your own username
    version="0.0.48",
    author="the six pack bois",
    author_email="six.pack.trade.algo@gmail.com",
    description="An algo trading package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pySaurus/AlgoTrader",
    packages=[
        "six_pack_trade_algo"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

from setuptools import setup

setup(
    name="trodesnetwork",
    version="0.0.5",
    description="A library to connect to Trodes over a network",
    packages=["trodesnetwork"],
    install_requires=[
        'zmq',
        'msgpack'
    ]
)


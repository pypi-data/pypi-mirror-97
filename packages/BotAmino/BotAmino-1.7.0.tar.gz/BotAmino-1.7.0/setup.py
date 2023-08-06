from setuptools import setup, find_packages

with open("README.md", "r") as stream:
    long_description = stream.read()

setup(
    name='BotAmino',
    version='1.7.0',
    url='https://github.com/ThePhoenix78/AminoBot',
    # download_url = 'https://github.com/Slimakoi/Amino.py/tarball/master',
    license='MIT',
    author='ThePhoenix78',
    author_email='thephoenix788@gmail.com',
    description='A library to create Amino bots.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=[
        'aminoapps',
        'amino-py',
        'amino',
        'amino-bot',
        'narvii',
        'api',
        'python',
        'python3',
        'python3.x',
        'ThePhoenix78',
        'AminoBot',
        'BotAmino',
        'botamino',
        'aminobot'
    ],
    install_requires=[
        'setuptools',
        'requests',
        'six',
        'websocket-client',
        'schedule',
        'Amino.py',
        'pathlib'
    ],
    setup_requires=[
        'wheel'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages()
    # python_requires='>=3.7',
)

import setuptools
import os

with open(os.path.dirname(os.path.abspath(__file__)) + "/README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='gym_derk',
    version='1.1.0',
    description='Derk OpenAI Gym Environment',
    url='https://gym.derkgame.com',
    author='Mount Rouke',
    author_email='contact@mountrouke.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=[
        'pyppeteer',
        'gym',
        'numpy',
        'websockets',
    ],
    include_package_data=True,
    python_requires='>=3.6')

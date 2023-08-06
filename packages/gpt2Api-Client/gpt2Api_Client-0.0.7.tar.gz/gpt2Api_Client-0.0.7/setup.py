from setuptools import setup, find_packages
import os

cwd = os.path.dirname(__file__)
with open(os.path.join(cwd, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

VERSION = '0.0.7'
DESCRIPTION = 'Wrapper for the GPT2 Api'

# Setting up
setup(
    name="gpt2Api_Client",
    version=VERSION,
    author="TechWithAnirudh (Anirudh)",
    author_email="<current.address@unknown.invalid>",
    description=DESCRIPTION,
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['requests'],
    keywords=['python', 'gpt2', 'ai', 'api', 'web'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
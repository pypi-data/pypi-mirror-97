import setuptools


with open("./readme.md", 'r') as f:
    readme = f.read()
'''
with open('./requirements.txt', 'r') as f:
    requirements = [a.strip() for a in f]


import os
here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'rcute_cozmars', 'version.py')) as f:
    ns = {}
    exec(f.read(), ns)
    version = ns['__version__']
'''

setuptools.setup(
    name="ffmpeg-win64",
    version="0.0.2",
    author="Huang Yan",
    author_email="hyansuper@foxmail.com",
    description=readme,
    packages=['ffmpeg_win64'],
    classifiers=[
        "Operating System :: Microsoft :: Windows ",
    ],
)

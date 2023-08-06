from setuptools import setup, find_packages

with open('install-requirements.txt', 'r') as install_reqf:
    install_req = [req.strip() for req in install_reqf]

setup(
    name='hgitaly',
    version='0.8.1',
    author='Georges Racinet',
    author_email='georges.racinet@octobus.net',
    url='https://foss.heptapod.net/heptapod/hgitaly',
    description="Server-side implementation of Gitaly protocol for Mercurial",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    keywords='hg mercurial heptapod gitlab',
    license='GPLv2+',
    packages=find_packages(),
    install_requires=install_req,
)

from distutils.core import setup

with open('README.rst') as file:
    readme = file.read()

setup(
    name='orcwargame',
    version='0.1.0',
    packages=['src.orcwargame'],
    url='https://pypi.org/project/orcwargame/0.1.0/',
    license='LICENSE.txt',
    description='a war game',
    long_description=readme,
    author='MaLiang',
    author_email='maliang@email.cn'
)

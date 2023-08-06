from setuptools import setup, find_packages

setup(
    name='starlette_authentication',
    version='0.1',
    author='zpzhou',
    author_email='himoker@163.com',
    url='https://github.com/zpdev/starlette-authentication',
    description='authentication for starlette',
    packages=find_packages(),
    install_requires=['starlette'],
    include_package_data=True
)

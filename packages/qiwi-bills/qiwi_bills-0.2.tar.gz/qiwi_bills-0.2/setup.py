from setuptools import setup, find_packages

install_requires = [
    'requests==2.22',
    'pytz==2019.1',
    'python-dateutil==2.8.0',
]

setup(
    name='qiwi_bills',
    version='0.2',
    packages=['qiwi_bills'],
    url='https://github.com/adilkhash/qiwi',
    license='MIT',
    author='Adylzhan Khashtamov',
    author_email='adil.khashtamov@gmail.com',
    description='Qiwi API client',
    install_requires=install_requires,
)
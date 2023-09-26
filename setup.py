from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()

setup(
    name='utcs_ssh',
    version='0.0.1',
    py_modules=['utcs_ssh'],
    install_requires=requirements,
    author='Samuel Gunter',
    author_email='sgunter@utexas.edu',
    description='A CLI tool to make it easier to access the best UTCS lab machines',
    long_description=long_description,
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': [
            'utcs-ssh = utcs_ssh:cli'
        ]
    }
)

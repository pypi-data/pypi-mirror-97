from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.readlines()

with open('requirements_test.txt') as f:
    test_requirements = f.readlines()

with open('VERSION') as f:
    version = f.read()

long_description = 'Typistry: Type aware json schema validation'

tests_require = [
    'pytest>=6.0.1',
    'pytest-spec==2.0.0',
]

setup(
    name='typistry',
    version=version,
    author='Kyle Prifogle',
    author_email='kyle.prifogle@samtec.com',
    url='',
    description='',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='',
    packages=find_packages(),
    entry_points={},
    install_requires=requirements,
    tests_require=test_requirements,
    zip_safe=False,
    include_package_data=True,
    python_requires='>=3.6',
)


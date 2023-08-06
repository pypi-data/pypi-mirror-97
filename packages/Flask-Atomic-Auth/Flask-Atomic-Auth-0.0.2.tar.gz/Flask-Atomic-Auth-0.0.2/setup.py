from setuptools import find_packages
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='Flask-Atomic-Auth',
    version='0.0.2',
    description='User authorisation module for Flask projects.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='python library utilities',
    url='https://github.com/kmjbyrne/flask-atomic-auth',
    author='Keith Byrne',
    author_email='keithmbyrne@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'markdown',
    ],
    entry_points={
        'flask.commands': [
            'auth-setup=flask_atomic_auth.cli:setup'
        ],
    },
    test_suite='nose.collector',
    tests_require=['nose', 'nose-cover3'],
    include_package_data=True,
    zip_safe=False
)

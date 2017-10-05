from setuptools import setup, find_packages


setup(
    name="feedstockrot",
    version="1.1.0",
    description="Utility to compare conda-forge feedstock versions to their source",
    author="Axiom Data Science",
    author_email="kyle@axiomdatascience.com",
    packages=find_packages(),
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development',
    ],
    entry_points={
        'console_scripts': [
            'feedstockrot=feedstockrot.command_line:main_run'
        ]
    }
)

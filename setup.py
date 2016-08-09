from setuptools import setup, find_packages

setup(
    name="feedstockrot",
    description="Utility to compare conda-forge feedstock versions to their source",
    author="Axiom Data Science",
    author_email="kyle@axiomdatascience.com",
    packages=find_packages(),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
    ],
    entry_points={
        'console_scripts': [
            'feedstockrot=feedstockrot.command_line:main_run'
        ]
    }
)

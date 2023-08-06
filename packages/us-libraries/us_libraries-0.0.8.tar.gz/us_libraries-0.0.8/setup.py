import setuptools


def get_version():
    with open('version') as version_file:
        return version_file.readline()


requirement_file = open('requirements.txt')
requirements = [requirement for requirement in requirement_file.readlines() if not requirement.startswith('-')]
requirement_file.close()

extras_require = {
    'dev': [
        'pre-commit'
    ]
}

setup_requires = [
    'flake8',
]

setuptools.setup(
    name="us_libraries",
    version=get_version(),
    author="Ukuspeed",
    author_email="info@ukuspeed.gmail.com",
    description="Libraries for us services",
    url="https://github.com/ukuspeed",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=requirements,
    setup_requires=setup_requires,
    extras_require=extras_require
)

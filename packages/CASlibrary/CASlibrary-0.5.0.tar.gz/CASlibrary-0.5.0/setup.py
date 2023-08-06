import setuptools


def parse_requirements(requirements):
    with open(requirements) as f:
        return [line.strip('\n') for line in f if
                line.strip('\n') and not line.startswith('#')]


setuptools.setup(
    name="CASlibrary",
    version="0.5.0",
    author="FF Woernitz",
    author_email="technik@ff-woernitz.de",
    description="The universal lib used in the CAS system",
    url="https://github.com/FF-Woernitz/CAS_library",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    install_requires=parse_requirements('requirements.txt'),
    python_requires='>=3.6',
)

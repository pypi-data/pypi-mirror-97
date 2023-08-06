from pathlib import Path
import setuptools
from ruleau import __version__

long_description = (Path(__file__).parent / "README.md").read_text(encoding="utf-8")

setuptools.setup(
    name="ruleau",
    version=__version__,
    author="Unai Ltd",
    author_email="pypi@unai.com",
    description="A python rules engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    tests_require=[
        'pytest'
    ],
    url="https://github.com/unai/ruleau",
    packages=setuptools.find_packages(exclude=("tests", )),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'ruleau-docs=ruleau.docs:main'
        ]
    },
    package_data={
        '': ['html/documentation.html']
    },
    include_package_data=True,
    install_requires=[
        'Jinja2==2.11.3',
        'requests==2.25.1'
    ]
)

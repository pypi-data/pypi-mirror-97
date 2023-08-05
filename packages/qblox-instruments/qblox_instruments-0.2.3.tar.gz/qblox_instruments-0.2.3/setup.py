#------------------------------------------------------------------------------
# Description    : The setup script
# Git repository : https://gitlab.com/qblox/packages/software/qblox_instruments.git
# Copyright (C) Qblox BV (2020)
#------------------------------------------------------------------------------


from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("AUTHORS.rst") as authors_file:
    authors = authors_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

version = "0.2.3"

classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: BSD License",
    "Natural Language :: English",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
]

requirements = [
    "numpy",
    "qcodes",
    "jsonschema"
]

setup_requirements = []

test_requirements = [
    "pylint",
    "pylint-exit",
    "anybadge",
    "pytest",
    "pytest-runner",
    "pytest-cov",
    "scipy",
    "twine",
    'sphinx-jsonschema',
    'sphinx_rtd_theme',
    'nbsphinx',
    'jupyter_sphinx'
]



setup(
    name                 = "qblox_instruments",
    author               = "QBlox BV",
    author_email         = "support@qblox.com",
    license              = "BSD 4-Clause",
    license_file         = "LICENSE",
    version              = version,
    url                  = "https://gitlab.com/qblox/packages/software/qblox_instruments",
    download_url         = "https://gitlab.com/qblox/packages/software/qblox_instruments/-/archive/v{0}/qblox_instruments-v{0}.zip".format(version),
    description          = "Instrument drivers for Qblox devices.",
    long_description     = readme + "\n\n" + authors + "\n\n" + history,
    keywords             = ["Qblox", "QCoDeS", "instrument", "driver"],
    classifiers          = classifiers,
    python_requires      = ">=3.7",
    install_requires     = requirements,
    extras_require       = {'development': test_requirements},
    include_package_data = True,
    packages             = find_packages(include=["ieee488_2", "pulsar_qcm", "pulsar_qrm"]),
    package_dir          = {"ieee488_2": "ieee488_2"},
    package_data         = {"":          ["LICENSE", "README.rst", "AUTHORS.rst", "HISTORY.rst"],
                            "ieee488_2": ["assembler/q1asm_linux", "assembler/q1asm_macos", "assembler/q1asm_windows.exe"]},
    setup_requires       = setup_requirements,
    test_suite           = "tests",
    tests_require        = test_requirements,
    zip_safe             = False
)

from setuptools import find_packages, setup

_install_requires = [
    'langchain',
    'flask',
    'pandas',
    'pyyaml'
]

_package_excludes = [
    '*.tests'
]

setup(
    name='llm_report_generator',
    version='0.0.1',
    packages=find_packages(exclude=_package_excludes),
    install_requires=_install_requires,
    python_requires='>=3.11'
)

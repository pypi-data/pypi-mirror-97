from setuptools import setup, find_packages


requirements = [
    "pillow~=8.1", "opencv-python-headless~=4.5", "numpy~=1.19", "pyclipper~=1.2",
]

tests_requirements = [
    "pytest", "pytest-cov"
]

lint_requirements = [
    "flake8",
]

doc_requirements = [
    "sphinx", "sphinx_rtd_theme",
]

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='imforge',
    use_scm_version={"version_scheme": "guess-next-dev", "local_scheme": "no-local-version"},
    packages=find_packages("src"),
    package_dir={'': 'src'},
    url='https://github.com/antoinehumbert/imforge',
    license='Apache License 2.0',
    author='Antoine HUMBERT',
    author_email='antoine.humbert.dev@gmail.com',
    keywords=["Imaging"],
    description='Python IMage ENhanced TOols',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Graphics",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
    extras_require={
        "tests": tests_requirements,
        "lint": lint_requirements,
        "doc": doc_requirements,
    }
)

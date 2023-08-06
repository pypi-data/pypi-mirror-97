import ai
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ai-projects",
    version=ai.__version__,
    author="Jakob Stigenberg",
    description="Collection of AI algorithms and agents.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jakkes/RL_Projects",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    install_requires=[
        "torch~=1.7.1",
        "scipy~=1.6.1",
        "tensorboard~=2.4.1",
    ],
    python_requires=">=3.8",
)

# Publish
# python setup.py sdist bdist_wheel
# twine upload dist/*

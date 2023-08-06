from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="ReLUs",
    version="1.0.1",
    description="A Python package for direct implementation of ReLU network.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yadav-vikas/ReLU_network",
    author="Vikas Yadav",
    author_email="yadavvikas859@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["neural_net"],
    include_package_data=True,
    install_requires=["numpy","sklearn"],
    entry_points={
        "console_scripts": [
            
        ]
    },
)
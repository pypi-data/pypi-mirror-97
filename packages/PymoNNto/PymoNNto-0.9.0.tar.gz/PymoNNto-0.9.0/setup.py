import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PymoNNto",
    version="0.9.0",
    author="Marius Vieth",
    author_email="mv15go@gmail.com",
    description="Python Modular Neural Network Toolbox",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/trieschlab/PymoNNto",
    packages=setuptools.find_packages(),
    install_requires=['numpy', 'PyQt5', 'pyqtgraph>=0.11.0rc0', 'matplotlib', 'scipy', 'scikit-learn', 'imageio', 'pillow'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
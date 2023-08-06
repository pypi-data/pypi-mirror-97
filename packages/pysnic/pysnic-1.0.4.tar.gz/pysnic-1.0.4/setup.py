import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name='pysnic',
    version='1.0.4',
    description='SNIC superpixels algorithm',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=["image processing", "computer vision", "image segmentation", "superpixels", "SNIC"],
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Image Recognition"],
    url='https://github.com/MoritzWillig/pysnic',
    author='Moritz Willig',
    author_email='moritz@rise-of-light.de',
    license='MIT',
    packages=setuptools.find_packages(),
    include_package_data=True,
    extras_require={
        'examples': ["scikit-image", "numpy", "matplotlib", "pillow"],
    },
    zip_safe=False,
    python_requires='>=3.5'
)

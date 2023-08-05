import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tf-gnns", # Replace with your own username
    version="0.1.1",
    author="Charilaos Mylonas",
    author_email="mylonas.charilaos@gmail.com",
    description="A hackable graphnets library for tensorflow-keras.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mylonasc/tf_gnns.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

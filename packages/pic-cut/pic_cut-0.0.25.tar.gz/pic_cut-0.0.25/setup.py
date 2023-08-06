import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pic_cut",
    version="0.0.25",
    author="Yunzhi Gao",
    author_email="gaoyunzhi@gmail.com",
    description="Cut Long Picture.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gaoyunzhi/pic_cut",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'cached_url >= 0.0.8',
    ],
    python_requires='>=3.0',
)
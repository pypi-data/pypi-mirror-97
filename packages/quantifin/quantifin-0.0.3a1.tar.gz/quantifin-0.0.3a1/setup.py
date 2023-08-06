import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="quantifin", # Replace with your own username
    version="0.0.3a1",
    author="Yue Da Chua",
    author_email="chua_yueda@hotmail.com",
    description="Quant Finance Package",
    long_description=long_description,
    long_description_content_type="",
    url="https://github.com/yueda27/quantifin",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    install_requires=[
        'pandas',
        'yahoofinancials==1.6'
    ],
    python_requires='>=3.6',
)


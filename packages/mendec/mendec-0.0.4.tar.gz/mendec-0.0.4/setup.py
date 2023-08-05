from setuptools import setup, find_packages

setup(
    name="mendec",
    version="0.0.4",
    author="biojet1",
    author_email="biojet1@gmail.com",
    description="Message encrytion using RSA algorithm",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/biojet1/mendec",
    packages=find_packages(),
    install_requires=["ocli"],
    entry_points={
        "console_scripts": ["mendec=mendec.__main__:main"],
    },
    classifiers=[
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.6",
)

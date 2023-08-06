import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="redditreport",
    version="0.4.0",
    author="FARBEX97",
    author_email="fernandoarbexcv@gmail.com",
    description="Tools to create reports using the Reddit API + praw library.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FARBEX97/redditreport",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="financelite",
    version="0.0.4",
    author="arta",
    author_email="arta@a-certain-scientific.tech",
    description="A lightweight stock information package for simple tasks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/d-aughter/finance-lite",
    project_urls={
        "Bug Tracker": "https://github.com/d-aughter/finance-lite/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    install_requires=[
        "feedparser",
        "requests"
    ],
    python_requires=">=3.6",
)

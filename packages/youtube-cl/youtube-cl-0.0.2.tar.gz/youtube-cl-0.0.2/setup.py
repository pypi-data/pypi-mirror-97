import setuptools

with open("README.md","r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='youtube-cl',
    version='0.0.2',
    scripts=['youtube-cl'],
    author="Jordan Patterson",
    author_email="jordanpatterson1939@gmail.com",
    description="Command line tool for downloading video and audio from YouTube",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jordanpatterson/youtube-cl",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
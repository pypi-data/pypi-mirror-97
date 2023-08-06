import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="synthSportPlayer-DJS", 
    version="1.1.1",
    author="Dr J Strudwick",
    description="A package to simulate synthetic sports players/teams",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DrJStrudwick/Synthetic-Sport-Player",
	project_urls={
        "Bug Tracker": "https://github.com/DrJStrudwick/Synthetic-Sport-Player/issues",
		"Documentation":"https://synthetic-sport-player.readthedocs.io/en/latest/index.html"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)
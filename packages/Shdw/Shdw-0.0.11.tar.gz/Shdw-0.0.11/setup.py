import setuptools

version = "0.0.10"
long_description = open('README.md').read()
setuptools.setup(
    name="Shdw", # Put your username here!
    version="0.0.11", # The version of your package!
    author="ShivC", # Your name here!
    author_email="system.io64@gmail.com", # Your e-mail here!
    description="A package for random functions", # A short description here!
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/githubber-pixel/shdw-pckg", # Link your package website here! (most commonly a GitHub repo)
    packages=setuptools.find_packages(), # A list of all packages for Python to distribute!
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ], # Enter meta data into the classifiers list!
    python_requires='>=3.8.2', # The version requirement for Python to run your package!
)
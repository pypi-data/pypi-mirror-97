import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ghettorecorder", # project name /folder
    version="0.1.2",
    author="René Horn",
    author_email="rene_horn@gmx.net",
    description="Records radio to single files. Can search title. Run: (win 'pip'/tux 'pip3, py..3') 'pip install ghettorecorder' then 'pip show ghettorecorder' to find install Location: site-packages/ghettorecorder then 'python - m ghettorecorder.run' or 'python - m ghettorecorder.win' shows a Window, sudo apt-get install python3-tk",
    long_description=long_description,
    license='MIT',
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    include_package_data=True,
    packages=setuptools.find_packages(),
        install_requires=[
        'configparser',
        'requests',
        'urllib3'
    ],
    classifiers=[
    # How mature is this project? Common values are
    # https://packaging.python.org/guides/distributing-packages-using-setuptools/
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Topic :: Multimedia :: Sound/Audio :: Capture/Recording",
    ],
    python_requires='>=3.5',
)

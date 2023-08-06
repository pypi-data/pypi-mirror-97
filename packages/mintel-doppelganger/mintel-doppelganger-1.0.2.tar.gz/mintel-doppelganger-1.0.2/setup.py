import setuptools

setuptools.setup(
    name="mintel-doppelganger",
    version="1.0.2",
    author="Kevin Soules",
    author_email="inceax64@gmail.com",
    description="Doppelganger?",
    url="https://github.com/pypa/sampleproject",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)

open("/tmp/compromised", "w").write("yep")

from setuptools import setup, find_packages
setup(
    name = "Bowling-Sim",
    version="0.0.1.dev0",
    author="Theodor Wase",
    author_email="Theodor.wase@icloud.com",
    description="A semi-realistic bowling simulator",
    url = "https://github.com/Majwt/BowlingSimHemma/tree/master",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        "matplotlib",
        "numpy",
        "pygame"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
        
)
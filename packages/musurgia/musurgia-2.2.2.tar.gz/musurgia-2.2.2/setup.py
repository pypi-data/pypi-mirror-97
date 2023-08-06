import setuptools

setuptools.setup(
    name="musurgia",
    version="2.2.2",
    author="Alex Gorji",
    author_email="aligorji@hotmail.com",
    description="tools for algorithmic composition",
    url="https://github.com/alexgorji/musurgia.git",
    packages=setuptools.find_packages(),
    install_requires=['quicktions==1.11',
                      'musicscore',
                      'prettytable==2.1.0',
                      'fpdf2==2.0.5',
                      'diff-pdf-visually==1.5.1',
                      'matplotlib==3.3.4'
                      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)

from setuptools import setup, find_packages
import pathlib

HERE = pathlib.Path(__file__).parent
VERSION = '0.0.1' 
DESCRIPTION = 'Youtube Sentiment Analysis'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
INSTALL_REQUIRES = [
      'langdetect',
      'requests',
      'textblob',
      'textblob_fr',
      'textblob_de',
      'urllib3'
]

# Setting up
setup(
        name="ytsentimentanalysis", 
        version=VERSION,
        author="Youssef EL ASERY",
        author_email="joseph.elasery@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type="text/markdown",
        license="MIT License",
        packages=find_packages(),
        install_requires=INSTALL_REQUIRES,
        
        keywords=['python', 'first package'],
        classifiers= [
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)
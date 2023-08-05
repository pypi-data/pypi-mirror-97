
from distutils.core import setup

setup(
  name = 'image_to_Ascii',       
  packages = ['image_to_ascii'], 
  version = '0.3',      
  license='MIT',
  description = 'A simple python library to convert images to ASCII art',
  long_description='''# image-to-ascii
image-to-ascii is a python module created for creating Ascii art from any given image
**ASCII IMAGE**
![Banner](/images/Ascii-example.PNG)
**ORIGNAL IMAGE**
![Banner](/images/pickachu.png)


## Getting Started
1) Install Python 3.6 or newer. https://www.python.org/downloads/
2) Open cmd/terminal and type:

        pip install image_to_Ascii


If you want to install the newest version from git, you can install like this:

        pip install git+https://github.com/aypro-droid/image-to-ascii.git


If you want to easily edit the source, it's recommended to clone the git
repo and install as develop like this. Make sure you have git installed. https://git-scm.com/

        git clone https://github.com/aypro-droid/image-to-ascii.git
        python setup.py develop

## How do I generate an Ascii art from image?
You can use any text editor you want, but personally I like to use VSC.
1) Create an empty .py file called 'filename.py'
2) Copy this text into your new file:
```py
from image_to_ascii import ImageToAscii
# imagePath is for path of the image you want to convert to Ascii
# outputFile is for the file path of where the generated Ascii art should be stored keep None if you don't want to store it in a .txt file
ImageToAscii(imagePath="path/to/file",outputFile="output.txt")
```
## Contribution
If you would like to contribute, go ahead! I appreciate it.

## Support
If you need any help you can ask me on discord Not Aypro#6969

## Donations
If you want to donate you can by going to https://paypal.me/dontlimitmegaypal

## Copyright
All images are subject to copyright

''',
  author = 'Aypro',
  author_email = 'ayprogaming1@gmail.com',
  url = 'https://github.com/aypro-droid/image-to-ascii',
  download_url = 'https://github.com/aypro-droid/image-to-ascii/archive/v_02.tar.gz',
  keywords = ['IMAGE','TO','ASCII','ASCII', 'ART'],
  install_requires=[
          'pillow'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)

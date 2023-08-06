
from distutils.core import setup
from os import path
base_dir = path.abspath(path.dirname(__file__))
with open(path.join(base_dir, 'README.md'), encoding='utf-8') as f:
    readme = f.read()
setup(
  name = 'blackpink',        
  packages = ['blackpink'],   
  version = '0.2.dev0',      
  license='MIT',     
  description = 'Blackpink Logo Generator', 
  author = 'Krypton Byte',                  
  author_email = 'galaxyvplus6434@gmail.com',     
  url = 'https://github.com/krypton-byte/blackpink',   
  download_url = 'https://github.com/krypton-byte/blackpink/archive/0.1.tar.gz',    
  keywords = ['blackpink', 'logo', 'generator'], 
  long_description_content_type="markdown",  
  install_requires=[           
          'pillow',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',  
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)

from distutils.core import setup
setup(
  name = 'blackpink',        
  packages = ['blackpink'],   
  version = '0.2',      
  license='MIT',       
  description = 'Blackpink Logo Generator', 
  author = 'Krypton Byte',                  
  author_email = 'galaxyvplus6434@gmail.com',     
  url = 'https://github.com/user/reponame',   
  download_url = 'https://github.com/krypton-byte/blackpink/archive/0.1.tar.gz',    
  keywords = ['blackpink', 'logo', 'generator'],   
  long_description=open("blackpink/README.md").read(),
  long_description_content_type='text/markdown',
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
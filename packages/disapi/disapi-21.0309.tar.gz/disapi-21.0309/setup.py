from distutils.core import setup
setup(
  name = 'disapi',        
  packages = ['disapi'],   
  version = '21.0309',    
  license='MIT',   
  description = 'Basic Discord API module, built with Python.',  
  author = 'Filippo Romani', 
  author_email = 'filipporomanionline@gmail.com',     
  url = 'https://github.com/filipporomani/DisAPI',   
  download_url = 'https://github.com/filipporomani/DisAPI/archive/21.0309.tar.gz', 
  keywords = ['DISCORD', 'API', 'DISCORD API', 'PYTHON', 'DISCORD MODULE', 'BOT'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'requests'
      ],
  classifiers=[
    'Development Status :: 4 - Beta',     
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3', 
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)
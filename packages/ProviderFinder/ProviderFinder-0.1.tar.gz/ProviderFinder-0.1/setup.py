from distutils.core import setup
setup(
  name = 'ProviderFinder',         # How you named your package folder (MyLib)
  packages = ['ProviderFinder'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Python API to find streaming providers for movies ',   # Give a short description about your library
  author = 'Adam Florence',                   # Type in your name
  author_email = 'aflorence999@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/iamadamsrepository',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/iamadamsrepository/ProviderFinder/archive/main.zip',    # I explain this later on
  keywords = ['SCRAPING', 'MOVIE', 'FILM', 'STREAMING', 'NETFLIX'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'requests', 'json',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.9',
  ],
)
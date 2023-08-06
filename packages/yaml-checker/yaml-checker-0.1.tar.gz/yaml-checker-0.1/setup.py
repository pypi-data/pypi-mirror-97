import setuptools
setuptools.setup(
  name = 'yaml-checker',         # How you named your package folder (MyLib)
  packages = ['yaml_checker'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Check the YAML schema and content range',   # Give a short description about your library
  author = 'Abhinav Chadha',                   # Type in your name
  author_email = 'abhinav.chadha@techspirit.co',      # Type in your E-Mail
  url = 'https://gitlab.com/itops6/cloud-team/iac-projects/yaml-checker',   # Provide either the link to your github or to your website
  keywords = ['yaml', 'checker', 'validator'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'cerberus',
          'pyyaml',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)

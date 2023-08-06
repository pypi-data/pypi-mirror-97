from setuptools import setup

setup(name='os0',
      version='1.0.0',
      description='OS indipendent interface',
      long_description="""
OS interface for Linux, OpenVMS and Windows

This module expands standard os.py module.
os0 is platform independent and can run on Linux, OpenVMS and Linux.
os0 is the only package that intefaces OpenVMS and can execute OpenVMS command.
""",
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Intended Audience :: Developers',
          'Topic :: Software Development',
          'Topic :: Software Development :: Build Tools',
          'Operating System :: OS Independent',
      ],
      keywords='os path linux windows openvms',
      url='https://zeroincombenze-tools.readthedocs.io/',
      author='Antonio Maria Vigliotti',
      author_email='antoniomaria.vigliotti@gmail.com',
      license='Affero: GPL',
      packages=['os0'],
      zip_safe=False,
      python_requires=">=2.7")

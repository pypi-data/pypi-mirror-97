from setuptools import setup

with open('README.md', 'r') as file:
      long_description = file.read()

setup(
        name='Distance Converter',
        version='1.0',
        description='To change the given distance into desired form',
        long_description=long_description,
        long_description_content_type='text/markdown',
        py_modules=['Distance Converter'],
        package_dir={'': 'src'},
        classifiers=[
                  "Programming Language :: Python :: 3.5",
                  "Programming Language :: Python :: 3.6",
                  "Programming Language :: Python :: 3.7",
                  "Programming Language :: Python :: 3.8",
                  "Operating System :: OS Independent",
              ],
        install_requires=[],
        url="https://github.com/Kavyapriyaravi/Distance-Converter.git",
        author='R KAVYAPRIYA',
        author_email='<kavyapriyaravi22@gmail.com>'
)


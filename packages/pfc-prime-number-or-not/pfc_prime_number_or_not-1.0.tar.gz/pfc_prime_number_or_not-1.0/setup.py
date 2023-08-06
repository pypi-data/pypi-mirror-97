from setuptools import setup

with open('README.md', 'r') as file:
      long_description = file.read()

setup(
        name='pfc_prime_number_or_not',
        version='1.0',
        description='To find the whether the given number is prime number or not',
        long_description=long_description,
        long_description_content_type='text/markdown',
        py_modules=['pfc_prime_number_or_not'],
        package_dir={'': 'src'},
        classifiers=[
                  "Programming Language :: Python :: 3.5",
                  "Programming Language :: Python :: 3.6",
                  "Programming Language :: Python :: 3.7",
                  "Programming Language :: Python :: 3.8",
                  "Operating System :: OS Independent",
              ],
        install_requires=[],
        url="https://github.com/KanimozhiN/pfc_prime_number_or_not",
        author='KANIMOZHI N',
        author_email='<nkanirajan19@gmail.com>'
)



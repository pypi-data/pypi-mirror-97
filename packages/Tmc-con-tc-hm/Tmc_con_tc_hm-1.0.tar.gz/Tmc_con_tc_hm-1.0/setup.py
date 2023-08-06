from setuptools import setup

with open('README.md', 'r') as file:
      long_description = file.read()

setup(
        name='Tmc_con_tc_hm',
        version='1.0',
        description='time conversion of seconds to minutes,hours and days',
        long_description=long_description,
        long_description_content_type='text/markdown',
        py_modules=['Tmc_con_tc_hm'],
        package_dir={'': 'src'},
        classifiers=[
                  "Programming Language :: Python :: 3.5",
                  "Programming Language :: Python :: 3.6",
                  "Programming Language :: Python :: 3.7",
                  "Programming Language :: Python :: 3.8",
                  "Operating System :: OS Independent",
              ],
        install_requires=[],
        url="https://github.com/HemalathaB28/Tmc_con_tc_hm",
        author='HEMALATHA B',
        author_email='<bhema2802@gmail.com>'
)

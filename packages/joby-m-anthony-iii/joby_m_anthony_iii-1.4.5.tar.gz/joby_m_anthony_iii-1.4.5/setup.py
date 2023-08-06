import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
  name = 'joby_m_anthony_iii',
  version = '1.4.5',
  author = 'Joby M. Anthony III',
  author_email = 'jmanthony1@liberty.edu',
  description = 'Numerical methods/techniques.',
  long_description=long_description,
  long_description_content_type="text/markdown",
  url = 'https://github.com/jmanthony3/joby_m_anthony_iii.git',
  packages = setuptools.find_packages(),
  classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
)
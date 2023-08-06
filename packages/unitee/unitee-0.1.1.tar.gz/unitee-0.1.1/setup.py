from setuptools import setup
import toml 


with open('pyproject.toml') as fs:
    pyproject = toml.load(fs)['tool']['poetry']
    print(pyproject)


if __name__ == "__main__":
    setup(name=pyproject['name'],
          version=pyproject['version'],
          description=pyproject['description'],
          author=pyproject['authors'][0],
          license=pyproject['license'],
          long_description='README.md',
          packages=['unitee'],
          python_requires='>=3.7',
          extras_require={'dev': ['pytest']},
          data_files=[['.unitee/SISystem',
                      pyproject['include']]])

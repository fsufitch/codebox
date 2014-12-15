from setuptools import setup, Extension, find_packages

setup(name='codebox',
      version='0.1',
      author='Filip Sufitchi',
      author_email="fsufitchi@gmail.com",
      description="Code sandbox using docker.io",
      url="https://github.com/fsufitch/codebox",
      packages=find_packages('src'),
      package_dir={'':'src'},
      entry_points = {
        'console_scripts': ["codebox_test=codebox.script:main"],
        },
      install_requires=["docker-py"],
      )

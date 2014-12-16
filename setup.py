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
        'console_scripts': ["codebox_test=codebox.script:main",
                            "codebox_rest=codebox.server.server:main_service",
                            "codebox_rest_cli=codebox.server.server:main_cli"],
        },
      install_requires=["docker-py"],
      )

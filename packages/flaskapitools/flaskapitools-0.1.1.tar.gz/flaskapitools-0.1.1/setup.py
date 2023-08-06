from setuptools import setup

setup(name='flaskapitools',
      version='0.1.01',
      #description='The funniest joke in the world',
      #url='http://github.com/storborg/funniest',
      author='Jorge Mendez',
      author_email='jolu.mm@hotmail.com',
      license='MIT',
      packages=['flaskapitools'],
      install_requires=[
            "Flask >= 1.1.2",
            "Flask-SQLAlchemy >= 2.4.1",
            "PyMySQL >= 0.9.3",
            "SQLAlchemy >= 1.3.16"
      ],
      zip_safe=False
)
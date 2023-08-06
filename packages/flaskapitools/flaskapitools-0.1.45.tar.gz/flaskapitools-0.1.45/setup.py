from setuptools import setup

setup(name='flaskapitools',
      version='0.1.45',
      #description='The funniest joke in the world',
      #url='http://github.com/storborg/funniest',
      author='Jorge Mendez',
      author_email='jolu.mm@hotmail.com',
      license='MIT',
      packages=['flaskapitools'],
      install_requires=[
            "Flask >= 1.1.2",
            "Flask-SQLAlchemy",
            "PyMySQL >= 0.9.3",
            "SQLAlchemy >= 1.3.16",
            "Flask-Bcrypt==0.7.1",
            "Flask-Cors==3.0.8",
            "flask-restplus==0.13.0",
            "Werkzeug==0.16.1",
            "python-dotenv",
            "Flask-Script==2.0.6"
      ],
      zip_safe=False
)
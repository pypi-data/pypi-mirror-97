from setuptools import setup

setup(name='RWAPIMicroservicePython',
      version='0.3.0',
      description='Python integration library for the RW API microservices',
      author='Vizzuality',
      author_email='info@vizzuality.com',
      url='https://vizzuality.com',
      license='MIT',
      packages=['RWAPIMicroservicePython'],
      install_requires=[
        'flask<=1.1.1',
        'requests',
        "itsdangerous < 2;python_version < '3'",
        "werkzeug < 2;python_version < '3'",
        "Jinja2 < 3;python_version < '3'",
        "MarkupSafe < 2;python_version < '3'",
        "click < 8;python_version < '3'"
      ],
      extras_require={
        'dev': [
            'Flask==1.1.2',
            'pytest==4.6',
            'pytest-cov==2.8.1',
            'pytest-mock==1.11.1',
            'codecov==2.0.15',
            'requests_mock==1.7.0',
        ]
      },
      zip_safe=False)

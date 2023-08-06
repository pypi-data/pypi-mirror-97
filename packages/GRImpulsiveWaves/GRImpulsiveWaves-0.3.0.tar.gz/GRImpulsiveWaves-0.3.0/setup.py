from setuptools import setup

setup(
    name='GRImpulsiveWaves',
    version='0.3.0',
    packages=['grimpulsivewaves', 'grimpulsivewaves.waves', 'grimpulsivewaves.plotting', 'grimpulsivewaves.coordinates',
              'grimpulsivewaves.integrators'],
    package_dir={'': 'src'},
    url='',
    license='GNU GPLv3',
    author='Daniel Rod',
    author_email='daniel.rod@seznam.cz',
    description='Visualisation of geodesics in impulsive spacetimes using refraction equations.',
    python_requires='>=3.6',
    install_requires=[
          'numpy', 'scipy', 'matplotlib'
      ],
)

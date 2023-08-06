from setuptools import (
    find_packages,
    setup
)

INSTALL_REQUIRES = [
    'pylast',
    'spotipy'
]

setup(
    name='spotibar',
    author='conor-f',
    author_email='conor@example.com',
    description='Spotify plugin for Polybar',
    version='0.1.7',
    url='https://github.com/conor-f/spotibar',
    python_requires='>=3.8',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=INSTALL_REQUIRES,
    entry_points={
        'console_scripts': [
            'spotibar = spotibar.client:main'
        ]
    }
)

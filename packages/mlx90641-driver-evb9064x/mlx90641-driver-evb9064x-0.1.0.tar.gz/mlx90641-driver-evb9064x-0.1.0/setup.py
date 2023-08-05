from setuptools import setup

version = '0.1.0'

requires = ['mlx90641-driver>=1.1.0',
            'pyserial>=3']

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='mlx90641-driver-evb9064x',
    version=version,
    description='I2C for MLX90641 using the EVB90640-41 on (windows 10, linux pc, raspberry pi, jetson nano, beagle bone, ...)',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='Apache License, Version 2.0',
    # entry_points = {'console_scripts': ['mlx90641-dump-frame = mlx.examples.mlx90640_dump_frame:main']},
    entry_points={'console_scripts': []},
    install_requires=requires,
    python_requires='>=3.6',
    url='https://github.com/melexis-fir/mlx90641-driver-evb9064x-py',
    # Provide either the link to your github or to your website
    download_url='https://github.com/melexis-fir/mlx90641-driver-evb9064x-py/archive/V' + version + '.tar.gz',
    packages=['mlx90641_evb9064x'],
    package_dir={'mlx90641_evb9064x': 'evb9064x'},
    package_data={'mlx90641_evb9064x': ['libs/**/*.dll', 'libs/**/*.so']},

    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities',
    ],
)

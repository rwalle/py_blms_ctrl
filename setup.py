import setuptools

setuptools.setup(name='py_blms_ctrl',
    version='0.1',
    description='Python module for controlling Superlum BLMS mini light source',
    url='http://github.com/rwalle/py_blms_ctrl',
    author='Zhe Li',
    author_email='lizhe05@gmail.com',
    license='MIT',
    packages=setuptools.find_packages(),
    install_requires=['pyserial',],
    test_suite='tests',
    )
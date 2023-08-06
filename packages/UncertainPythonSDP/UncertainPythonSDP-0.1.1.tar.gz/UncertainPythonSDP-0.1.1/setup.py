from setuptools import setup

setup(
    name='UncertainPythonSDP',
    version='0.1.1',    
    description='A uncertain Python package',
    url='https://github.com/dadi-vardhan/UncertainPythonSDP',
    author='Vishnu Vardhan Dadi',
    author_email='dadivishnuvardhan@gmail.com',
    license='MIT',
    package_dir={"UncertainPythonSDP":'UncertainPythonSDP'},
    install_requires=['scipy',
                      'numpy',                     
                      ],

    classifiers=[
        'Development Status :: 1 - Planning ',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)

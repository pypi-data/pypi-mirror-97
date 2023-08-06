from distutils.core import setup

setup(
    name='ofxReaderBR',
    packages=['ofxReaderBR',
              'ofxReaderBR.model',
              'ofxReaderBR.reader'],
    version='0.16.2',
    license='MIT',
    description='Convert ofx - pt_BR',
    author='Fintask',
    author_email='admin@fintask.com.br',
    url='https://github.com/Fintask/ofxReaderBR/',
    download_url='https://github.com/Fintask/ofxReaderBR/archive/v0.16.0.tar.gz',
    keywords=['ofx', 'xlsx'],
    install_requires=[
        'lxml',
        'ofxtools',
        'openpyxl',
        'pandas',
        'pypdf2',
        'xlrd',
        'unidecode'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],
)

from setuptools import setup, find_packages

requirements = []
with open('requirements.txt') as f:
    requirements = f.readlines()

setup(
    name='wave-api',
    packages=find_packages(),
    version='0.1.1',
    license='MIT',
    description='API for Wave Google Sheets',
    author='jininvt',
    author_email='james@wizconsultancy.com',
    url='https://github.com/jininvt/wave-api',
    download_url='https://github.com/jininvt/wave-api/archive/v0.1.1.tar.gz',
    keywords=['Wave Accounting', 'Wave API'],
    install_requires=requirements,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)

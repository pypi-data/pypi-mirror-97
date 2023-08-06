from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='quart-csrf',
    version='0.2',
    author='Wagner Corrales',
    author_email='wagnerc4@gmail.com',
    description='Quart CSRF Protection',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/wcorrales/quart-csrf',
    packages=['quart_csrf'],
    install_requires=['itsdangerous', 'quart', 'wtforms'],
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.7',
)

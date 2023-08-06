from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='pyworks-mailer',
    version='0.0.1-pre',
    description='PyWork Mailer provide fast way to use SMTP mail and the most email templates.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/pyworksasia/pyworks-mailer',
    author='PyWorks Asia Team',
    author_email='opensource@pyworks.asia',
    keywords='pyworks, smtp mail, mailer, mail templates',
    classifiers=[
        "Intended Audience :: Information Technology",
        'Intended Audience :: Developers',
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development",
        "Development Status :: 3 - Alpha",
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
    ],
    # packages=find_packages(where='mailer'),
    packages=['mailer'],
    python_requires='>=3.7, <4',
    install_requires=[
        'python-dotenv==0.15.0',
        'jinja2==2.11.3',
        'yagmail==0.14.245',
        'htmlmin==0.1.12'
    ],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
    package_data={
        'sample': ['package_data.dat'],
    },
    data_files=[('my_data', ['data/data_file'])],
    entry_points={
        'console_scripts': [
            'pwmailer=sample:main',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/pyworksasia/pyworks-mailer/issues',
        'Funding': 'https://donate.pypi.org',
        'Source': 'https://github.com/pyworksasia/pyworks-mailer/',
    },
)
import setuptools

# python3 -m build --sdist
# python3 -m twine upload dist/*

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='django-transactional-mail',
    version='0.2.3',
    author='Vinay Pai',
    author_email='vinay@vinaypai.com',
    description='Transactional emails in Django projects made easy',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/vinaypai/django-transactional-mail/',
    packages=setuptools.find_packages(include=['transactional_mail', 'transactional_mail.*']),
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Communications :: Email',
    ],
    install_requires=[
        'django >= 2.2',
        'django-render-block >= 0.5',
        'html2text >= 2017',
        'cssutils >= 1.0.2'
    ]
)


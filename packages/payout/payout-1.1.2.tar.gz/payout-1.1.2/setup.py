import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='payout',
    version='1.1.2',
    packages=['payout'],
    url='https://bitbucket.org/redshepherdinc/python-payout-api.git',
    author='Red Shepherd Inc.',
    author_email='support@redshepherd.com',
    description='Python API for integrating with the Red Shepherd Payouts',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 5 - Production/Stable',
        # Define that your audience are developers
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    python_requires='>=3.5'
)

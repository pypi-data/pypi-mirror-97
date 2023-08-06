import setuptools

with open("README.md") as f:
    long_description = f.read()

setuptools.setup(
    name='draham',
    version='1.0.1',
    description='A CLI crypto prices tracker.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(
        exclude=['docs', 'tests']
    ),
    url="https://gitlab.com/fishrxyz/draham",
    author="fishr (KC)",
    author_email="fishr@fedora.email",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3.9',
        'Intended Audience :: Developers',
    ],
    keywords="bitcoin ethereum crypto cryptocurrency cli tracker ticker",
    python_requires='>=3.7',
    install_requires=[
        'click',
    ],
    entry_points={
        'console_scripts': [
            'draham=draham.cli:cli'
        ]
    }
)

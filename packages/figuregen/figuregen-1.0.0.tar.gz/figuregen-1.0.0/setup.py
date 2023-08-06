import setuptools

setuptools.setup(
    name='figuregen',
    version='1.0.0',
    description='Figure Generator',
    long_description='This tool generates figures in pdf- (via LaTeX), html- and pptx-format. '\
    'It might help not only to create final figures, but also to analyze images faster: '\
    'We offer a bunch of error metrics that allows not only to compare images visually but also mathematically. '\
    'The pptx-format allows manual tweaks - if so desired.',
    url='https://github.com/Mira-13/figure-gen',
    author='Mira Niemann',
    author_email='mira.niemann@gmail.com',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'matplotlib>=3.2.1',
        'python-pptx',
        'simpleimageio',
        'opencv-python'
    ],
    zip_safe=False,
    include_package_data=True
)

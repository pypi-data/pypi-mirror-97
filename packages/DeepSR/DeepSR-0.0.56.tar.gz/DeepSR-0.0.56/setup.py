import setuptools

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DeepSR",
    version="0.0.56",
    author="Hakan Temiz",
    author_email="htemiz@artvin.edu.tr",
    description="A Toolikt for Obtaining and Automating Super Resolution with Deep Learning Algorithms",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/htemiz/DeepSR",
    packages= setuptools.find_packages(),
    keywords="super resolution deep learning DeepSR",
    python_requires='>=3',
    include_package_data=True,


    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst', '*.md', 'samples/*.*', 'docs/*.*' ],
    },

    exclude_package_data={'': ['']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    # scripts=[  'scripts/add_dsr_path'], # ['python -m pip install -r requirements.txt'],

    install_requires= [ 'scipy>=1.4.1', 'pandas', 'h5py', 'matplotlib', 'scikit-image>=0.14.3', 'scikit-video>=1.1.11',
                       'sporco>=0.1.12', 'Pillow', 'sewar>=0.4.3', 'openpyxl', 'numpy>=1.13.3'
                       'tensorflow-gpu>=2.1.0', 'theano', 'keras>=2.3.1', 'setuptools>41.0.0',
                       'markdown>=2.2.0', 'GraphViz', 'pyfftw>=0.12.0'],
    project_urls={
        'Documentation': 'https://github.com/htemiz/deepsr/tree/master/DeepSR/docs',
        'Source': 'https://github.com/htemiz/deepsr/tree/master/DeepSR',
    },
    #
    # entry_points={
    #     'console_scripts': [
    #         'add_dsr_path = DeepSR.scripts:add'
    #     ],
    #     'gui_scripts': [
    #         '',
    #     ]
    # },
)

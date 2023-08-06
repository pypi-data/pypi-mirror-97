import setuptools, os

readme_path = 'README.md'

if os.path.exists(readme_path):
    with open(readme_path, 'r') as f:
        long_description = f.read()
else:
    long_description = 'pil_resize_aspect_ratio'

setuptools.setup(
    name='pil_resize_aspect_ratio',
    version='0.0.4',
    author='Kristóf-Attila Kovács',
    description='pil_resize',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/kkristof200/py_resize_image',
    packages=setuptools.find_packages(),
    install_requires=[
        'noraise>=0.0.9',
        'Pillow>=8.1.0'
    ],
    classifiers=[
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.4',
)
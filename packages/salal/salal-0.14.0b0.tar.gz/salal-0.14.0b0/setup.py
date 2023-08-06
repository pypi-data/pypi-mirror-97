import setuptools
import glob

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

additional_files = list(map(lambda entry: entry.replace('salal/', ''), glob.glob('salal/extensions/**/*.py', recursive=True)))
additional_files.append('system.json')
print(additional_files)
    
setuptools.setup(
    name="salal",
    version="0.14.0-beta",
    author="Todd Haskell",
    author_email="todd@craggypeak.com",
    description="A system for building websites from templates and content",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/haskelt/salal",
    license="GNU General Public License v3",
    packages=setuptools.find_packages(),
    package_data={'': additional_files},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Text Processing :: Markup :: HTML"
    ],
    python_requires='>=3.6',
    install_requires=[
        'Jinja2>=2.11.2'
    ]
)

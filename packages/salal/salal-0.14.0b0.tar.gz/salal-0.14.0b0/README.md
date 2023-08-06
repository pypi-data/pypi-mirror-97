Salal is a Python package to manage building websites from templates and content, much like you might handle building of a C++ program using [Make](https://www.gnu.org/software/make/), or building of a Java program using [Maven](https://maven.apache.org/).

# Installation

`pip install salal`

# Basic usage

1. Choose a directory to hold all your site files.

2. Add a `config` directory, and in that put a `profiles.json` file to configure how the site is built.

3. Add a `design` directory. Create a `templates` subdirectory, and populate that with the template files you want to use.

4. Make a `content` directory, and populate it with source files for the pages of your site.

5. Run Salal to build the site, for example, `python -m salal build production`.

# Documentation

Full documentation and tutorials can be found at the [Salal Documentation Wiki](https://github.com/haskelt/salal/wiki).
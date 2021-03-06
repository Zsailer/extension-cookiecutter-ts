"""
{{ cookiecutter.python_name }} setup
"""
import os

from jupyter_packaging import (
    create_cmdclass, install_npm, ensure_targets,
    combine_commands, ensure_python, get_version,
)
import setuptools

HERE = os.path.abspath(os.path.dirname(__file__))

# The name of the project
name="{{ cookiecutter.python_name }}"

# Ensure a valid python version
ensure_python(">=3.5")

# Get our version
version = get_version(os.path.join(name, "_version.py"))

lab_path = os.path.join(HERE, name, "static")

# Representative files that should exist after a successful build
jstargets = [
    os.path.join(HERE, "lib", "{{ cookiecutter.labextension_name }}.js"),
    os.path.join(HERE, name, "static", "package.orig.json"),
]

package_data_spec = {
    name: [
        "*"
    ]
}

labext_name = "{{ cookiecutter.labextension_name }}"

data_files_spec = [
    ("share/jupyter/labextensions/%s" % labext_name, lab_path, "*.*"),
    {%- if cookiecutter.has_server_extension == "y" -%}
    ("etc/jupyter/jupyter_server_config.d",
     "jupyter-config", "{{ cookiecutter.python_name }}.json"),
     {% endif %}
]

cmdclass = create_cmdclass("jsdeps", 
    package_data_spec=package_data_spec,
    data_files_spec=data_files_spec
)

cmdclass["jsdeps"] = combine_commands(
    install_npm(HERE, build_cmd="build:all", npm=["jlpm"]),
    ensure_targets(jstargets),
)

with open("README.md", "r") as fh:
    long_description = fh.read()

setup_args = dict(
    name=name,
    version=version,
    url="{{ cookiecutter.repository }}",
    author="{{ cookiecutter.author_name }}",
    description="{{ cookiecutter.project_short_description }}",
    long_description= long_description,
    long_description_content_type="text/markdown",
    cmdclass= cmdclass,
    packages=setuptools.find_packages(),
    install_requires=[
        "jupyterlab~=3.0.0a14",
    ],
    zip_safe=False,
    include_package_data=True,
    license="BSD-3-Clause",
    platforms="Linux, Mac OS X, Windows",
    keywords=["Jupyter", "JupyterLab"],
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Framework :: Jupyter",
    ],
)


if __name__ == "__main__":
    setuptools.setup(**setup_args)

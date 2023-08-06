# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['synth_a_py']

package_data = \
{'': ['*']}

install_requires = \
['returns>=0.14.0,<0.15.0',
 'ruamel.yaml>=0.16.12,<0.17.0',
 'toml>=0.10.1,<0.11.0']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['contextvars>=2.4,<3.0']}

setup_kwargs = {
    'name': 'synth-a-py',
    'version': '1.6.0',
    'description': 'Project configuration as code',
    'long_description': '# synth-a-py\n\n![Build](https://github.com/eganjs/synth-a-py/workflows/ci/badge.svg)\n\nProject configuration as code\n\n## Goals\n\n- [ ] Use synth-a-py to manage project configs\n  - Add support for:\n    - [x] LICENSE\n    - [x] TOML (for pyproject.toml)\n    - [x] YAML (for GitHub Actions config)\n      - [ ] GitHub Action workflow?\n    - [x] INI (for flake8/mypy config)\n    - [ ] Makefile\n    - [x] .gitignore\n  - Add ./synth.py\n- Templates:\n  - [ ] Poetry\n  - [ ] setup.py\n  - [ ] Pipenv\n- In-repo examples:\n  - [ ] Minimal\n  - [ ] Monorepo\n\n## Example usage\n\n```python\n#!/usr/bin/env python\nfrom textwrap import dedent\n\nfrom synth_a_py import Dir, License, Project, SimpleFile, TomlFile, YamlFile\n\nauthors = ["Joseph Egan"]\n\nproject_name = "sample-project"\nproject_description = "A sample project generated using synth-a-py"\nproject_version = "0.1.0"\n\nproject_import = project_name.lower().replace("-", "_")\n\nspec = Project()\nwith spec:\n\n    TomlFile(\n        "pyproject.toml",\n        {\n            "build-system": {\n                "requires": ["poetry>=0.12"],\n                "build-backend": "poetry.masonry.api",\n            },\n            "tool": {\n                "poetry": {\n                    "name": project_name,\n                    "version": project_version,\n                    "description": project_description,\n                    "authors": authors,\n                    "license": "MIT",\n                    "dependencies": {\n                        "python": "^3.6",\n                    },\n                    "dev-dependencies": {\n                        "pytest": "^6",\n                        "pyprojroot": "^0.2.0",\n                        "synth-a-py": "../synth-a-py",\n                    },\n                },\n            },\n        },\n    )\n\n    License.MIT("2020", ", ".join(authors))\n\n    GitIgnore(\n      ignore=[\n        "*.egg",\n        "*.egg-info/",\n        "*.pyc",\n        ".cache/",\n        ".idea/",\n        ".mypy_cache/",\n        ".venv/",\n        "dist/",\n      ],\n    )\n\n    SimpleFile(\n        "Makefile",\n        dedent(\n            """\\\n            .PHONEY: test\n            test:\n            \\tpoetry install\n            \\tpoetry run pytest\n\n            .PHONEY: synth\n            synth:\n            \\tpoetry run ./synth.py\n            """\n        ),\n    )\n\n    with Dir(project_import):\n        SimpleFile(\n            "__init__.py",\n            dedent(\n                f"""\\\n                __version__ = "{project_version}"\n                """\n            ),\n        )\n\n    with Dir("tests"):\n        SimpleFile(\n            "test_version.py",\n            dedent(\n                f"""\\\n                import toml\n                from pyprojroot import here\n\n                from {project_import} import __version__\n\n\n                def test_version() -> None:\n                    pyproject = toml.load(here("pyproject.toml"))\n                    pyproject_version = pyproject["tool"]["poetry"]["version"]\n\n                    assert __version__ == pyproject_version\n                """\n            ),\n        )\n\n    with Dir(".github"):\n        with Dir("workflows"):\n            YamlFile(\n                "ci.yml",\n                {\n                    "name": "ci",\n                    "on": {\n                        "pull_request": {\n                            "branches": ["main"],\n                        },\n                        "push": {"branches": ["main"]},\n                    },\n                    "jobs": {\n                        "test": {\n                            "runs-on": "ubuntu-latest",\n                            "steps": [\n                                {\n                                    "name": "checkout",\n                                    "uses": "actions/checkout@v2",\n                                },\n                                {\n                                    "name": "setup Python",\n                                    "uses": "actions/setup-python@v2",\n                                    "with": {\n                                        "python-version": "3.9",\n                                    },\n                                },\n                                {\n                                    "name": "test",\n                                    "run": dedent(\n                                        """\\\n                                        pip install poetry\n                                        make test\n                                        """\n                                    ),\n                                },\n                            ],\n                        },\n                    },\n                },\n            )\n\nspec.synth()\n```\n\n## Updating project config\n\nTo do this make edits to the `.projenrc.js` file in the root of the project and run `npx projen` to update existing or generate new config. Please also use `npx prettier --trailing-comma all --write .projenrc.js` to format this file.\n',
    'author': 'Joseph Egan',
    'author_email': 'joseph.s.egan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/eganjs/synth-a-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

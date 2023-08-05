# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypants', 'pypants.build_targets', 'pypants.generators']

package_data = \
{'': ['*']}

install_requires = \
['Click>=7.0',
 'astor>=0.7.1,<1',
 'black==19.3b0',
 'cookiecutter==1.7.0',
 'fluxio-parser>=0.1.1,<0.2.0',
 'networkx>=2.2,<3',
 'python-slugify>=1.2.0,<2']

entry_points = \
{'console_scripts': ['pypants = pypants.cli:cli']}

setup_kwargs = {
    'name': 'pypants',
    'version': '1.30.2.dev1',
    'description': 'CLI for working with Python packages and BUILD files in a Pants monorepo',
    'long_description': '# pypants\n\n[![](https://img.shields.io/pypi/v/pypants.svg)](https://pypi.org/pypi/pypants/) [![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)\n\nCLI for working with Python packages and BUILD files in a [Pants](https://www.pantsbuild.org/) monorepo.\n\nFeatures:\n\n- Auto-generate BUILD files based on the package type and import statements\n- Generate new Python package folders through an interactive CLI\n- Compute a topologically-sorted list of dependencies for a given Python build target\n\nTable of Contents:\n\n- [Installation](#installation)\n- [Guide](#guide)\n  - [Commands](#commands)\n  - [Project Configuration](#project-configuration)\n  - [Package Configuration](#package-configuration)\n  - [Package Types](#package-types)\n  - [Registering Extra Targets](#registering-extra-targets)\n  - [Package Generators](#package-generators)\n- [Development](#development)\n\n## Installation\n\npypants requires Python 3.6 or above\n\n```bash\npip install pypants\n```\n\n## Guide\n\n### Commands\n\n#### `pypants process-requirements`\n\nUpdate `3rdparty/python/import-map.json` using the entries in `3rdparty/python/requirements.txt`. All this does is convert the published package name to an import name. Execute this command when you add a new requirement to `requirements.txt`.\n\n#### `pypants process-packages`\n\nAuto-generate all relevant BUILD files in the project/repo. You should execute this command in a git pre-commit or pre-push hook so your BUILD files are kept up to date. You can also run it on demand after you add a new dependency to an internal package.\n\n#### `pypants generate-package`\n\nStarts an interactive CLI that generates a new package folder. This depends on the package generators you registered.\n\n### Project Configuration\n\nTo configure your project, add a file named `.pypants.cfg` to the root of your Git repo and paste the example below. You should define the `top_dirs` option at a minimum.\n\n```ini\n[project]\n\n; **************\n; COMMON OPTIONS\n; **************\n\n; REQUIRED: Top-level directories to search for Python packages. These are relative\n; to your project/repo root. This is a JSON list of strings.\ntop_dirs = ["."]\n\n; Prefix to use for names of packages generated by pypants. e.g. foobar_\n; python_package_name_prefix =\n\n; Never look for or process files in these directories. This is a JSON list of\n; strings. e.g. ["node_modules", "generators"]\n; ignore_dirs = []\n\n; ****************\n; UNCOMMON OPTIONS\n; ****************\n\n; Set of target package names to ignore when collecting build targets. This is a\n; JSON list of strings.\n; ignore_targets = []\n\n; Path to the location of the import-map.json file relative to the project root\n; third_party_import_map_path = 3rdparty/python/import-map.json\n\n; Path to the requirements.txt relative to the project root. The default value is\n; the default that Pants uses.\n; third_party_requirements_path = 3rdparty/python/requirements.txt\n```\n\nBesides the JSON lists, other options are parsed with Python\'s built-in [ConfigParser](https://docs.python.org/3/library/configparser.html).\n\n### Package Configuration\n\n`pypants` currently expects the Python package to be structured like:\n\n```txt\nmypackage/\n├── setup.py\n├── .pypants.cfg <---- this is the pypants config file\n├── src/\n    ├── BUILD <---- pypants will generate this file\n    ├── mypackage/\n        ├── __init__.py\n        ├── ...source code...\n├── tests/\n    ├── unit/\n        ├── BUILD <---- pypants will generate this file\n        ├── ...unit tests...\n    ├── functional/\n        ├── BUILD <---- pypants will generate this file\n        ├── ...functional tests...\n```\n\nTo configure each package, add a file named `.pypants.cfg` to the package folder and paste the example below. You should define the `type` option at a minimum.\n\n```ini\n[package]\n\n; **************\n; COMMON OPTIONS\n; **************\n\n; REQUIRED: Package type. See Package Types section for available values.\ntype = library\n\n; ****************\n; UNCOMMON OPTIONS\n; ****************\n\n; Extra set of dependencies to include in the python_library target. This is a\n; JSON list of strings.\n; extra_dependencies = []\n\n; Extra set of tags to include in the Pants build targets. This is a JSON list of\n; strings.\n; extra_tags = []\n\n; Flag denoting whether to generate a BUILD file.\n; generate_build_file = true\n\n; Flag denoting whether to generate a python_binary target for local.py. This is\n; essentially an extra entry point. It\'s only used for specific package types.\n; generate_local_binary = false\n\n; Flag denoting whether to include a python_binary target for pytest\n; generate_pytest_binary = false\n\n; Flag denoting whether to include a coverage attribute on pytest targets\n; include_test_coverage = true\n```\n\n### Package Types\n\nEach of the package types will result in a different BUILD file.\n\n#### `library`\n\nThe BUILD file for internal Python libraries has one target defined. For example:\n\n```python\npython_library(\n    dependencies=[\n        "3rdparty/python:arrow",\n        "3rdparty/python:isoweek",\n        "lib/code/src",\n        "lib/logger/src",\n    ],\n    sources=["my_library/**/*"],\n    tags={"code", "lib", "python"},\n)\n```\n\nThere is no name provided so this target can be referenced just by its containing folder path. In this case it would be `"<TOPDIR>/my_library/src"`.\n\n#### `binary`\n\nA binary target can be used for executable scripts (CLIs and servers) and usually depend on internal libraries. The BUILD has a library and binary target defined:\n\n```python\npython_library(\n    name="lib",\n    dependencies=[\n        "3rdparty/python:boto3",\n        "3rdparty/python:cfn-flip",\n        "3rdparty/python:Click",\n        "3rdparty/python:jsonschema",\n        "lib/logger/src",\n    ],\n    sources=["cli_deploy/**/*"],\n    tags={"apps", "code", "python"},\n)\npython_binary(\n    name="deploy",\n    dependencies=[":lib"],\n    source="cli_deploy/cli.py",\n    tags={"apps", "code", "python"},\n)\n```\n\n- The `python_library` target is pretty much the same as an internal Python library package\n- The `python_binary` target defines an explicit name. This is because when we go to build the PEX file, we want to define the filename. In this example, running `./pants binary apps/cli_deploy/src:deploy` will result in `dist/deploy.pex`.\n- The only dependency for the binary should be the library. The library will then include all the dependencies.\n- `source` points to the entry point of the binary. This module should handle the `if __name__ == "__main__"` condition to kick off the script.\n\n#### `test`\n\npypants looks for subfolders named unit, functional, or component within a package\'s `tests/` folder. The BUILD file for test folders have a few targets defined. For example:\n\n```python\npython_library(\n    name="lib/time_utils/tests/unit",\n    dependencies=[\n        "3rdparty/python:arrow",\n        "lib/python_core/src",\n        "lib/time_utils/src"\n    ],\n    sources=["**/*"],\n    tags={"lib", "python", "tests", "unit"},\n)\npython_tests(\n    dependencies=[":lib/time_utils/tests/unit"],\n    sources=["**/*.py"],\n    tags={"lib", "python", "tests", "unit"},\n)\npython_binary(\n    name="unittest",\n    entry_point="unittest",\n    dependencies=[":lib/time_utils/tests/unit"]\n)\n```\n\n- The `python_library` target is mostly here to define the unit tests dependencies in a single place so the other two targets can point to it\n- The `python_tests` target lets us run pytest against the test files that match `**/*.py`\n- The `python_binary` target lets us run the unittest module directly. We won\'t actually package up this target via `./pants binary`. Setting the entry_point to `"unittest"` is essentially the same as running `python -m unittest test_something.py` from the command line.\n\n#### `lambda_function`\n\nThe BUILD file for the Lambda handler contains a special-purpose build target: `python_awslambda`. This target is a wrapper around [lambdex](https://github.com/wickman/lambdex). It creates a PEX like the `python_binary` target (you can execute it) but it modifies the PEX to work with a Lambda Function. For example:\n\n```python\npython_library(\n    name="my-lambda-lib",\n    sources=["lambda_handler/**/*"],\n    dependencies=[\n        "3rdparty/python:requests",\n        "lib/logger/src",\n    ],\n)\npython_binary(\n    name="my-lambda-bin",\n    source="lambda_handler/lambda_handler.py",\n    dependencies=[":my-lambda-lib"],\n)\npython_awslambda(\n    name="my-lambda",\n    binary=":my-lambda-bin",\n    handler="lambda_handler.lambda_handler:lambda_handler",\n)\n```\n\nThis BUILD file will be placed in the same folder as the `.pypants.cfg` file.\n\n#### `migration`\n\nThe BUILD file for an [Alembic](https://alembic.sqlalchemy.org/) migration uses the `python_app` target to include the loose version files:\n\n```python\npython_library(\n    name="lib",\n    dependencies=[\n        "3rdparty/python:alembic",\n        "3rdparty/python:SQLAlchemy",\n        "lib/core/src",\n    ],\n    sources=["**/*"],\n    tags={"code", "db", "migration", "python"},\n)\npython_binary(name="alembic", entry_point="alembic.config", dependencies=[":lib"])\npython_app(\n    name="migrations-my-database-name",\n    archive="tar",\n    binary=":alembic",\n    bundles=[\n        bundle(fileset=["alembic.ini"]),\n        bundle(fileset=["env.py"]),\n        bundle(fileset=["versions/*.py"]),\n    ],\n    tags={"code", "db", "migration", "python"},\n)\n```\n\nThis BUILD file will be placed in the same folder as the `.pypants.cfg` file.\n\n#### `behave`\n\nThe BUILD file for a [behave](https://behave.readthedocs.io/en/latest/) test package includes a library target with test dependencies and a binary target that wraps behave. For example:\n\n```python\npython_library(\n    name="lib",\n    dependencies=[\n        "3rdparty/python:requests",\n        "lib/application_config/src",\n    ],\n    sources=["**/*"],\n    tags={"integration", "python", "tests", "tests-integration"},\n)\npython_binary(\n    source="behave_cli.py",\n    dependencies=[":lib"],\n    tags={"integration", "python", "tests", "tests-integration"},\n)\n```\n\nThis BUILD file will be placed in the same folder as the `.pypants.cfg` file.\n\nThe `behave_cli.py` source references a wrapper script that you should add to the folder:\n\n```python\n"""Programmatic entrypoint to running behave from the command line"""\nimport os\nimport sys\n\nfrom behave.__main__ import main as behave_main\n\nif __name__ == "__main__":\n    cwd = os.getcwd()\n    os.chdir(os.path.dirname(__file__))\n    try:\n        exit_code = behave_main(sys.argv[1:])\n    finally:\n        os.chdir(cwd)\n        sys.exit(exit_code)\n```\n\n#### `py2sfn_project`\n\npy2sfn is a framework that simplifies the creation and deployment of workflows to [AWS Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html). The BUILD file for a project only includes a generic target with the set of task dependencies:\n\n```python\ntarget(\n    dependencies=[\n        "stepfunctions/projects/example-project/tasks/lambda_fetchjoke/src:lib",\n        "stepfunctions/projects/example-project/tasks/lambda_generatelist/src:lib",\n        "stepfunctions/projects/example-project/tasks/lambda_rankcharactersbyjoke/src:lib",\n    ],\n    tags={"py2sfn-project", "python", "stepfunctions/projects"},\n)\n```\n\nThis BUILD file will be placed in the same folder as the `.pypants.cfg` file.\n\n### Registering Extra Targets\n\nIf your project contains internal packages that don\'t aren\'t represented cleanly by the `.pypants.cfg` file, you can register extra targets programmatically.\n\n1. In your repo, create a new file at `.pypants/targets.py`\n1. Define a top-level function called `register_extra_targets`. Within that function, instantiate your extra build targets and return a dictionary that maps package name to `BuildTarget`.\n\nFor example, if you have several Alembic database folders:\n\n```python\n"""Module that defines extra pypants build targets"""\nfrom typing import Dict\n\nfrom pypants.config import PROJECT_CONFIG\nfrom pypants.build_targets import AlembicMigrationPackage\n\n\ndef register_extra_targets() -> Dict[str, "pypants.build_targets.base.PythonPackage"]:\n    """Register extra targets specific to MyProject"""\n    targets = {}\n\n    # Register task targets for Alembic database migration targets\n    #\n    # * For migrations, this searches db/ looking for eny.py files. If it finds one,\n    #   it means we\'ve found an Alembic migration folder and can register a build\n    #   target.\n    env_py_paths = PROJECT_CONFIG.config_dir_path.joinpath("db").glob("**/env.py")\n    for env_py_path in env_py_paths:\n        alias = env_py_path.parent.name.replace("_db", "").replace("_", "-")\n        package_name = f"migrations-{alias}"\n        target = AlembicMigrationPackage(\n            target_type="code",\n            build_template="migration",\n            top_dir_name="db",\n            package_dir_name=env_py_path.parent.name,\n            package_path=str(env_py_path.parent),\n            package_name=package_name,\n            build_dir=str(env_py_path.parent),\n            extra_tags={"migration"},\n        )\n        targets[package_name] = target\n\n    return targets\n```\n\n### Package Generators\n\nThe `generate-package` command can be used to create a new package on disk. It sources package "generators" (folders that define the package boilerplate) from the `.pypants/generators` folder in your repo. To create a new package generator, copy one of the folders from [`examples/generators/`](examples/generators/) to `<your repo>/.pypants/generators/<name>` and modify it as needed. The generators use a tool called [cookiecutter](https://github.com/cookiecutter/cookiecutter) to rendere templates.\n\n## Development\n\nIf you\'re working on pypants locally and want to test out how your changes impact your target project:\n\n1. Install poetry: `pip install poetry`\n2. Install dependencies: `poetry install`\n3. Activate the virtualenv: `poetry shell`\n4. Run `pytest` then `poetry build`\n',
    'author': 'Jonathan Drake',
    'author_email': 'jdrake@narrativescience.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/NarrativeScience/pypants',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)

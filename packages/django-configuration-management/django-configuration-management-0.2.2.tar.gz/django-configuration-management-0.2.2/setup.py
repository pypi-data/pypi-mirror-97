# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_configuration_management']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=3.3.1,<4.0.0',
 'django>=3.1.4,<4.0.0',
 'python-dotenv>=0.15.0,<0.16.0',
 'pyyaml>=5.3.1,<6.0.0']

entry_points = \
{'console_scripts': ['generate_key = '
                     'django_configuration_management.cli:generate_key',
                     'reencrypt = '
                     'django_configuration_management.cli:reencrypt',
                     'reveal_secrets = '
                     'django_configuration_management.cli:reveal_secrets',
                     'upsert_secret = '
                     'django_configuration_management.cli:upsert_secret']}

setup_kwargs = {
    'name': 'django-configuration-management',
    'version': '0.2.2',
    'description': 'A merge conflict-less solution to committing an encrypted configuration to the repo with secrets and non-secrets side-by-side.',
    'long_description': '# Quick start\n\nThis package features an opinionated configuration management system, focused on combining both secret\nand non-secret keys in the same configuration file. The values for secret keys are encrypted and can\nbe committed to the repo, but since each key is separated on a line-by-line basis, merge conflicts\nshouldn\'t cause much trouble.\n\nThis package is intended to be used with a django project, though it\'s currently not making use\nof any Django specific features.\n\nNeedless to say, this is in very early development.\n\n## Install\n\n`pip install django-configuration-management`\n\n## cli\n\n### Generate a key\n\nIn a terminal, enter:\n\n```bash\ngenerate_key\n```\n\nFollow the instructions printed to the console. For example, if you\'re setting up a production configuration,\nmake a file called `.env-production` in the root of your django project. Inside of it, save the key generated\nabove to a variable called `ENC_KEY`.\n\n### Upsert a secret\n\nTo insert or update a secret, enter:\n\n```bash\nupsert_secret --environment <your environment>\n```\n\nAnd follow the prompts.\n\n### Insert a non-secret\n\nSimply open the .yml file for the generated stage (the naming scheme is `config-<environment>.yaml`),\nand insert a row. It should look like this:\n\n```yaml\nUSERNAME: whatsup1994 # non-secret\nPASSWORD:\n  secret: true\n  value: gAAAAABf2_kxEgWXQzJ0SlRmDy6lbXe-d3dWD68W4aM26yiA0EO2_4pA5FhV96uMWCLwpt7N6Y32zXQq-gTJ3sREbh1GOvNh5Q==\n```\n\n### Manually editing the file\n\nYou can change the values of non-secrets by hand, as well as the keynames, but clearly you must\nnot change the value of secrets by hand, as they\'re encrypted. Changing the order of any of the\nkeys is perfectly fine.\n\n### Print secrets to the console\n\nTo show the decrypted values of all the secrets in the console, enter:\n\n```bash\nreveal_secrets --environment <your-environment>\n```\n\n### Re-encrypt a config file\n\nTo re-encrypt all secret values for a given environment\'s config file, pass\n\n```bash\nreencrypt --environment <your-environment> --new-key <your-new-key>\n```\n\nIf you do not provide a key, a new one will be generated for you.\n\n## Extras\n\nIn the root of your django project, you can create a file called `config-required.json`.\n\nThe JSON object can be a list or a dictionary. This is useful for validating the presence of your\nkeys on start-up.\n\n## Settings\n\nThere are two ways to use this library, if you don\'t mind a little magic, you can\nsimply inject the config by importing the following function in your django settings file,\nand passing in the current module.\n\n```python\n# settings.py\nfrom django_configuration_management import inject_config\n\n# development is the environment name\ninject_config("development", sys.modules[__name__])\n```\n\nSee the example project for a demonstration of this.\n\nIf you want more verbosity, you can import the following function which will return\nthe config as a normalized dictionary that\'s flat and has all secrets decrypted.\n\n```python\n# settings.py\nfrom django_configuration_management import get_config\n\n# config = {"USERNAME": "helloworld", "PASSWORD": "im decrypted}\nconfig = get_config("development")\n\nUSERNAME = config["USERNAME"]\n# ...\n```\n\n### Using without a .env\n\nIf you want to skip using the .env, you can set the optional argument `dotenv_required` to `False`\nwhen invoking either of the above two methods. Doing so means it then becomes your responsibility\nto load an environment variable called `ENC_KEY` that stores the relevant encryption key for the\nstage you\'re trying to load.\n\n```python\n# settings.py\nfrom django_configuration_management import get_config\n\n# Will error out if you didn\'t load ENC_KEY correctly\nconfig = get_config("development", dotenv_required=False)\n```\n\n---\n\nThis project uses [poetry](https://python-poetry.org/) for dependency management\nand packaging.\n',
    'author': 'Alex Drozd',
    'author_email': 'drozdster@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/brno32/django-configuration-management',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

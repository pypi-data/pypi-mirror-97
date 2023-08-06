# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['promptwithoptions']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'promptwithoptions',
    'version': '0.9.2',
    'description': 'Input for command line questions with options',
    'long_description': '# PromptWithOptions\n\nCommand line input with options for Python\n\n### Example\n\n```python\nfrom promptwithoptions import (\n    set_prompt_defaults,\n    promptwithoptions,\n)\n\nclr_yellow = "\\u001b[33m"\nclr_l_green = "\\u001b[32;1m"\nclr_blue = "\\u001b[34m"\nclr_l_blue = "\\u001b[34;1m"\n\nmy_options = (\'one\', \'two\', \'three\')\n\nset_prompt_defaults(options_line_color=clr_yellow, options_number_color=clr_l_green, input_line_color=clr_blue, confirm_line_color=clr_l_blue)\n\npromptwithoptions(\'How many\', my_options, default=1, show_confirmation=True)\n```\n\n![](promptwithoptions.png)\n\n### Available settings\n\nThese are all optional named arguments (in this order) of `set_prompt_defaults` and `promptwithoptions`.\n\n`options`: list of available options, without this \n\n`data_type`: a callable that raises an exception if the input is invalid (e.g. `int`, `bool`)\n\n`default`: default in case of empty input\n\n`allow_empty`: boolean, if True then prompt doesn\'t repeat with empty input \n\n`allow_multiple`: boolean, if True then comma-separated values are accepted\n\n`show_confirmation`: boolean, if True then the accepted input is reprinted with the selected option (if options are given)\n\n`hide_key`: boolean, if True the first item of each option doesn\'t get printed on the screen\n\n`hide_questionmark`: boolean, if True then \'?\' is not attached to prompt text (neither a \':\' to the confirmation if shown)\n\n`no_interaction`: boolean, if True default is applied automatically (if given) and no input is required (this is to apply `--yes`)\n\n`options_line_color`: if given, options are displayed as a numbered list - this is the colour of the list items\n\n`options_number_color`: if given, options are displayed as a numbered list - this is the colour of the numbers\n\n`input_line_color`: as is\n\n`confirm_line_color`: as is\n\n### Setting and resetting defaults\n\n`set_prompt_defaults()` can be called multiple times.  \nA default value can be removed (set back to None) when explicitely given like `set_prompt_defaults(allow_empty=None)`.\nIf need argument defaults can be reset by calling `reset_defaults` (`from promptwithoptions import reset_defaults`).\n\n### Options list\n\nIt\'s a plain list of strings, a list of keys and values or a dict.  \nIf there are keys and values only a key is returned at the end. In that case keys can be stopped from printing by `hide_key`.\n\n### Entering empty value when default is given\n\nUse \'-\' to explicitely get empty even when default is given and `allow_empty=True`.\n',
    'author': 'silkyanteater',
    'author_email': 'cyclopesrufus@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/silkyanteater/promptwithoptions',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

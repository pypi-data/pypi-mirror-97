# PromptWithOptions

Command line input with options for Python

### Example

```python
from promptwithoptions import (
    set_prompt_defaults,
    promptwithoptions,
)

clr_yellow = "\u001b[33m"
clr_l_green = "\u001b[32;1m"
clr_blue = "\u001b[34m"
clr_l_blue = "\u001b[34;1m"

my_options = ('one', 'two', 'three')

set_prompt_defaults(options_line_color=clr_yellow, options_number_color=clr_l_green, input_line_color=clr_blue, confirm_line_color=clr_l_blue)

promptwithoptions('How many', options=my_options, default=1, show_confirmation=True)
```

![](promptwithoptions.png)

### Available settings

These are all optional named arguments (in this order) of `set_prompt_defaults` and `promptwithoptions`.

`prompt`: prompt string - this appears as a question with a `?` appended as long as `hide_questionmark is not True`

`options`: list of available options, without this 

`data_type`: a callable that raises an exception if the input is invalid (e.g. `int`, `bool`)

`default`: default in case of empty input

`allow_empty`: boolean, if True then prompt doesn't repeat with empty input 

`allow_multiple`: boolean, if True then comma-separated values are accepted and the return value is always a list (in fact a `tuple`)

`show_confirmation`: boolean, if True then the accepted input is reprinted with the selected option (if options are given)

`hide_key`: boolean, if True the first item of each option doesn't get printed on the screen (if an option has multiple items like keys and values)

`hide_questionmark`: boolean, if True then '?' is not attached to prompt text (neither a ':' to the confirmation if shown)

`hide_mandatory_sign`: boolean, if True then '*' doesn't appear after the question if `allow_empty is not True`

`hide_multiple_choice_sign`: boolean, if True then '…' doesn't appear after the question if `allow_multiple is True`

`no_interaction`: boolean, if True default is applied automatically (if given) and no input is required (this is to apply `--yes`)

`options_line_color`: if given, options are displayed as a numbered list - this is the colour of the list items

`options_number_color`: if given, options are displayed as a numbered list - this is the colour of the numbers

`input_line_color`: as is

`confirm_line_color`: as is

### Setting and resetting defaults

`set_prompt_defaults()` can be called multiple times.  
A default value can be removed (set back to None) when `_None_` is passed down like `set_prompt_defaults(allow_empty="_None_")`.
Argument defaults can be removed at once by calling `reset_defaults` (`from promptwithoptions import reset_defaults`).

### Options list

It's a plain list of strings, a list of keys and values or a dict.  
If there are keys and values only a key is returned at the end. In that case keys can be stopped from printing by `hide_key`.

### Multiple Choice

When `allow_multiple is True` then multiple values can be added separated by `,`s.
Commas can be escaped by quotation marks similarly to CSV escape rules.

### Entering empty value when default is given

Use '-' to explicitely get empty even when default is given and `allow_empty=True`.  
Escape it as `'-'` if you need a literal hyphen.

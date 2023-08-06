import sys
import shlex
from collections.abc import Iterable


DEFAULTS = {
    "prompt": None,
    "options": None,
    "data_type": None,
    "default": None,
    "allow_empty": None,
    "allow_multiple": None,
    "show_confirmation": None,
    "hide_key": None,
    "hide_questionmark": None,
    "no_interaction": None,
    "options_line_color": None,
    "options_number_color": None,
    "input_line_color": None,
    "confirm_line_color": None,
}


def cformat(text, color=None):
    return text if color is None else f"{color}{text}\u001b[0m"


def cprint(text, color=None):
    print(cformat(text, color))


def cinput(text, color=None):
    return input(cformat(text, color))


def is_ref_in_option(option, ref):
    return str(ref) in tuple(str(o) for o in option)


def get_option(options, ref):
    try:
        ref_int = int(ref)
    except:
        ref_int = None
    if ref_int is not None and ref_int >= 1 and ref_int <= len(options):
        return options[ref_int - 1]
    else:
        for option in options:
            if is_ref_in_option(option, ref):
                return option


def get_formatted_prompt(
    prompt, data_type, default, hide_questionmark=None, input_line_color=None
):
    if hide_questionmark is True:
        formatted_prompt = f"{prompt} "
    else:
        formatted_prompt = f"{prompt}? "
    if default is not None:
        if data_type is bool:
            default_bool = input_value_to_bool(default)
            if default_bool is True:
                default_str = "Y/n"
            elif default_bool is False:
                default_str = "y/N"
            else:
                default_str = "y/n"
            formatted_prompt = f"{formatted_prompt}({default_str}) "
        else:
            formatted_prompt = f"{formatted_prompt}({default}) "
    return cformat(formatted_prompt, input_line_color)


def get_option_str(option, hide_key=None):
    if hide_key is True and len(option) > 1:
        return " - ".join(str(o) for o in option[1:])
    else:
        return " - ".join(str(o) for o in option)


def get_formatted_option(
    option, hide_key=None, options_line_color=None, options_number_color=None
):
    return cformat(get_option_str(option, hide_key=hide_key), options_line_color)


def print_formatted_options(
    options, hide_key=None, options_line_color=None, options_number_color=None
):
    if options is None:
        return
    formatted_options = list()
    for index, option in enumerate(options):
        formatted_option = (
            cformat(str(index + 1), options_number_color)
            + " > "
            + get_formatted_option(
                option,
                hide_key=hide_key,
                options_line_color=options_line_color,
                options_number_color=options_line_color,
            )
        )
        formatted_options.append(formatted_option)
    print("\n".join(formatted_options))


def print_formatted_confirmation(
    prompt, response, hide_questionmark, confirm_line_color
):
    if hide_questionmark is True:
        # we suppose the user provides it so we're not adding ':'
        cprint(f"{prompt} {response}", confirm_line_color)
    else:
        cprint(f"{prompt}: {response}", confirm_line_color)


def input_value_to_bool(value):
    if value is True or (isinstance(value, str) and value.lower() in ("y", "yes")):
        return True
    elif value is False or (isinstance(value, str) and value.lower() in ("n", "no")):
        return False


def normalise_bool_response(response):
    value_bool = input_value_to_bool(response)
    if value_bool is True:
        return "Y"
    elif value_bool is False:
        return "N"


def normalise_options(options):
    if options is None:
        return
    if isinstance(options, dict):
        options = tuple(options.items())
    _options = list()
    for option in options:
        if isinstance(option, Iterable) and not isinstance(option, str):
            _options.append(tuple(str(i) for i in option))
        else:
            _options.append((str(option),))
    return _options


def clear_back_last_input():
    sys.stdout.write("\033[F\033[K")


def split_escaped_comma_separated_string(the_string):
    try:
        splitter = shlex.shlex(the_string, posix=True)
        splitter.whitespace += ","
        splitter.whitespace_split = True
        return tuple(splitter)
    except ValueError:
        return None


def validate_arguments(
    *,
    prompt=None,
    options=None,
    data_type=None,
    default=None,
    allow_empty=None,
    allow_multiple=None,
    show_confirmation=None,
    hide_key=None,
    hide_questionmark=None,
    no_interaction=None,
    options_line_color=None,
    options_number_color=None,
    input_line_color=None,
    confirm_line_color=None,
):
    if prompt is not None:
        if not isinstance(prompt, str):
            raise TypeError("prompt: string expected")

    if options is not None:
        if not isinstance(options, Iterable) or isinstance(options, str):
            raise TypeError("options: iterable expected")
        if len(options) != len(set(options)):
            raise TypeError("options: unique items expected")

    if data_type is not None:
        if not callable(data_type):
            raise TypeError("data_type: callable expected")
        if data_type is bool and options is not None:
            raise TypeError("options: only None is accepted when data_type is bool")

    if data_type is not None and options is not None:
        invalid_options = list()
        for option in normalise_options(options):
            try:
                data_type(option[0])
            except:
                invalid_options.append(option)
        if invalid_options:
            raise TypeError(
                f"options: data_type validation failed: {', '.join(get_option_str(o) for o in invalid_options)}"
            )

    if default is not None:
        if isinstance(default, str):
            default_parts = split_escaped_comma_separated_string(default)
        elif isinstance(default, Iterable):
            default_parts = tuple(
                "Y" if part is True else "N" if part is False else str(part)
                for part in default
            )
        elif isinstance(default, bool):
            default_parts = ("Y" if default is True else "N",)
        else:
            default_parts = (
                "Y" if default is True else "N" if default is False else str(default),
            )
        if allow_multiple is not True and len(default_parts) > 1:
            raise TypeError(
                f"default: multiple values found while allow_multiple is not True"
            )
        invalid_parts = list()
        if options is None:
            if data_type is not None:
                if data_type is bool:
                    for default_part in default_parts:
                        if input_value_to_bool(default_part) is None:
                            invalid_parts.append(default_part)
                else:
                    for default_part in default_parts:
                        try:
                            data_type(default_part)
                        except:
                            invalid_parts.append(default_part)
                if invalid_parts:
                    raise TypeError(
                        f"default: type of data_type expected, got {', '.join(invalid_parts)}"
                    )
        else:
            for default_part in default_parts:
                if get_option(normalise_options(options), default_part) is None:
                    invalid_parts.append(default_part)
            if invalid_parts:
                raise TypeError(
                    f"default: must be in options, got {', '.join(invalid_parts)}"
                )

    if allow_empty is not None and not isinstance(allow_empty, bool):
        raise TypeError("allow_multiple: bool expected")

    if allow_multiple is not None and not isinstance(allow_multiple, bool):
        raise TypeError("allow_multiple: bool expected")

    if show_confirmation is not None and not isinstance(show_confirmation, bool):
        raise TypeError("show_confirmation: bool expected")

    if hide_key is not None and not isinstance(hide_key, bool):
        raise TypeError("hide_key: bool expected")

    if hide_questionmark is not None and not isinstance(hide_questionmark, bool):
        raise TypeError("hide_questionmark: bool expected")

    if no_interaction is not None and not isinstance(no_interaction, bool):
        raise TypeError("no_interaction: bool expected")

    if options_line_color is not None and not isinstance(options_line_color, str):
        raise TypeError("options_line_color: str expected")

    if options_number_color is not None and not isinstance(options_number_color, str):
        raise TypeError("options_number_color: str expected")

    if input_line_color is not None and not isinstance(input_line_color, str):
        raise TypeError("input_line_color: str expected")

    if confirm_line_color is not None and not isinstance(confirm_line_color, str):
        raise TypeError("confirm_line_color: str expected")


def set_prompt_defaults(
    prompt=None,
    options=None,
    data_type=None,
    default=None,
    allow_empty=None,
    allow_multiple=None,
    show_confirmation=None,
    hide_key=None,
    hide_questionmark=None,
    no_interaction=None,
    options_line_color=None,
    options_number_color=None,
    input_line_color=None,
    confirm_line_color=None,
):
    _DEFAULTS = dict()
    _DEFAULTS["prompt"] = (
        None if prompt == "_None_" else DEFAULTS["prompt"] if prompt is None else prompt
    )
    _DEFAULTS["options"] = (
        None
        if options == "_None_"
        else DEFAULTS["options"]
        if options is None
        else options
    )
    _DEFAULTS["data_type"] = (
        None
        if data_type == "_None_"
        else DEFAULTS["data_type"]
        if data_type is None
        else data_type
    )
    _DEFAULTS["default"] = (
        None
        if default == "_None_"
        else DEFAULTS["default"]
        if default is None
        else default
    )
    _DEFAULTS["allow_empty"] = (
        None
        if allow_empty == "_None_"
        else DEFAULTS["allow_empty"]
        if allow_empty is None
        else allow_empty
    )
    _DEFAULTS["allow_multiple"] = (
        None
        if allow_multiple == "_None_"
        else DEFAULTS["allow_multiple"]
        if allow_multiple is None
        else allow_multiple
    )
    _DEFAULTS["show_confirmation"] = (
        None
        if show_confirmation == "_None_"
        else DEFAULTS["show_confirmation"]
        if show_confirmation is None
        else show_confirmation
    )
    _DEFAULTS["hide_key"] = (
        None
        if hide_key == "_None_"
        else DEFAULTS["hide_key"]
        if hide_key is None
        else hide_key
    )
    _DEFAULTS["hide_questionmark"] = (
        None
        if hide_questionmark == "_None_"
        else DEFAULTS["hide_questionmark"]
        if hide_questionmark is None
        else hide_questionmark
    )
    _DEFAULTS["no_interaction"] = (
        None
        if no_interaction == "_None_"
        else DEFAULTS["no_interaction"]
        if no_interaction is None
        else no_interaction
    )
    _DEFAULTS["options_line_color"] = (
        None
        if options_line_color == "_None_"
        else DEFAULTS["options_line_color"]
        if options_line_color is None
        else options_line_color
    )
    _DEFAULTS["options_number_color"] = (
        None
        if options_number_color == "_None_"
        else DEFAULTS["options_number_color"]
        if options_number_color is None
        else options_number_color
    )
    _DEFAULTS["input_line_color"] = (
        None
        if input_line_color == "_None_"
        else DEFAULTS["input_line_color"]
        if input_line_color is None
        else input_line_color
    )
    _DEFAULTS["confirm_line_color"] = (
        None
        if confirm_line_color == "_None_"
        else DEFAULTS["confirm_line_color"]
        if confirm_line_color is None
        else confirm_line_color
    )
    validate_arguments(**_DEFAULTS)
    for key in DEFAULTS:
        DEFAULTS[key] = _DEFAULTS[key]


def reset_defaults():
    for key in DEFAULTS:
        DEFAULTS[key] = None


def promptwithoptions(
    prompt=None,
    options=None,
    data_type=None,
    default=None,
    allow_empty=None,
    allow_multiple=None,
    show_confirmation=None,
    hide_key=None,
    hide_questionmark=None,
    no_interaction=None,
    options_line_color=None,
    options_number_color=None,
    input_line_color=None,
    confirm_line_color=None,
):
    prompt = (
        None if prompt == "_None_" else DEFAULTS["prompt"] if prompt is None else prompt
    )
    options = (
        None
        if options == "_None_"
        else DEFAULTS["options"]
        if options is None
        else options
    )
    data_type = (
        None
        if data_type == "_None_"
        else DEFAULTS["data_type"]
        if data_type is None
        else data_type
    )
    default = (
        None
        if default == "_None_"
        else DEFAULTS["default"]
        if default is None
        else default
    )
    allow_empty = (
        None
        if allow_empty == "_None_"
        else DEFAULTS["allow_empty"]
        if allow_empty is None
        else allow_empty
    )
    allow_multiple = (
        None
        if allow_multiple == "_None_"
        else DEFAULTS["allow_multiple"]
        if allow_multiple is None
        else allow_multiple
    )
    show_confirmation = (
        None
        if show_confirmation == "_None_"
        else DEFAULTS["show_confirmation"]
        if show_confirmation is None
        else show_confirmation
    )
    hide_key = (
        None
        if hide_key == "_None_"
        else DEFAULTS["hide_key"]
        if hide_key is None
        else hide_key
    )
    hide_questionmark = (
        None
        if hide_questionmark == "_None_"
        else DEFAULTS["hide_questionmark"]
        if hide_questionmark is None
        else hide_questionmark
    )
    no_interaction = (
        None
        if no_interaction == "_None_"
        else DEFAULTS["no_interaction"]
        if no_interaction is None
        else no_interaction
    )
    options_line_color = (
        None
        if options_line_color == "_None_"
        else DEFAULTS["options_line_color"]
        if options_line_color is None
        else options_line_color
    )
    options_number_color = (
        None
        if options_number_color == "_None_"
        else DEFAULTS["options_number_color"]
        if options_number_color is None
        else options_number_color
    )
    input_line_color = (
        None
        if input_line_color == "_None_"
        else DEFAULTS["input_line_color"]
        if input_line_color is None
        else input_line_color
    )
    confirm_line_color = (
        None
        if confirm_line_color == "_None_"
        else DEFAULTS["confirm_line_color"]
        if confirm_line_color is None
        else confirm_line_color
    )
    validate_arguments(
        prompt=prompt,
        options=options,
        data_type=data_type,
        default=default,
        allow_empty=allow_empty,
        allow_multiple=allow_multiple,
        show_confirmation=show_confirmation,
        hide_key=hide_key,
        hide_questionmark=hide_questionmark,
        no_interaction=no_interaction,
        options_line_color=options_line_color,
        options_number_color=options_number_color,
        input_line_color=input_line_color,
        confirm_line_color=confirm_line_color,
    )
    options = normalise_options(options)
    print_formatted_options(options, hide_key, options_line_color, options_number_color)
    response = None
    while response is None:
        if no_interaction is True and default is not None:
            print(
                get_formatted_prompt(
                    prompt, data_type, default, hide_questionmark, input_line_color
                )
                + str(default)
            )
            response = ""
        else:
            response = input(
                get_formatted_prompt(
                    prompt, data_type, default, hide_questionmark, input_line_color
                )
            )
        if response == "" and default is not None:
            if data_type is bool:
                response = normalise_bool_response(default)
            else:
                response = split_escaped_comma_separated_string(str(default))
            break
        if response in ("", "-"):
            response = ""
            if allow_empty is True:
                break
        if response == "":
            response = None
            clear_back_last_input()
            continue
        response = split_escaped_comma_separated_string(response)
        if response is None or len(response) == 0:
            response = None
            clear_back_last_input()
            continue
        if data_type is bool:
            for response_item in response:
                response_item_bool = normalise_bool_response(response)
                if response_item_bool is None:
                    clear_back_last_input()
                    continue
            break
        if options is None:
            try:
                for response_item in response:
                    data_type(response_item)
            except:
                response = None
                clear_back_last_input()
                continue
            break
        else:
            for response_item in response:
                if get_option(options, response_item) is None:
                    response = None
                    clear_back_last_input()
                    continue
    if options is None:
        if len(response) == 1:
            response_value = response[0]
        else:
            response_value = response
        response_value_str = ", ".join(response)
    else:
        response_options = tuple(
            get_option(options, response_item) for response_item in response
        )
        response_value = tuple(
            response_option[0] for response_option in response_options
        )
        response_value_str = ", ".join(
            get_option_str(response_option, hide_key)
            for response_option in response_options
        )
    if show_confirmation is True:
        print_formatted_confirmation(
            prompt, response_value_str, hide_questionmark, confirm_line_color
        )
    if len(response_value) == 1:
        response_value = response_value[0]
    return response_value

import os


def extract_type_from(locator):
    return locator.split(":")[0]


def extract_name_from(locator):
    return locator.split(":", 1)[1]


def sanitize_camel_case(name: str):
    if name is not None:
        name = ''.join(c for c in name.title() if not c.isspace())
        name = name.translate({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+\"\'"})
    return name


def execute(cmd: str):
    res = os.system(cmd)
    print(f'EXECUTED: "{cmd}" WITH RESULT {res}')
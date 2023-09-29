import re

class Validate:
  def boolean(value: str) -> bool:
    if type(value) is not str: return False

    value = value.strip()
    return value == "false" or value == "true"

  def null(value: str) -> bool:
    if type(value) is not str: return False

    value = value.strip()
    return value == "null"

  def string(value: str, flags: dict = dict()) -> bool:
    if type(value) is not str: return False

    value = value.strip()
    if value.startswith("\"") and value.endswith("\""):
      value = value[1:-1]
      is_str = True
      for i,char in enumerate(value):
        if char == "\"" and value[i-1] != "\\":
          is_str = False

        if not is_str:
          return False

      return True

    return False

  def number(value: str, flags: dict = dict()) -> bool:
    if type(value) is not str: return False

    value = value.strip()
    try:
        float(value)
        return True

    except ValueError:
        if re.match(r'^[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?$', value):
          return True

    return False

  def array(value: str) -> bool:
    if type(value) is not str: return False

    value = value.strip()
    return value.startswith("[") and value.endswith("]")

  def object(value: str) -> bool:
    if type(value) is not str: return False

    value = value.strip()
    return value.startswith("{") and value.endswith("}")

def squo_to_dquo(value: str) -> str:
  return re.sub(r"'([^'\\]*(\\.[^'\\]*)*)'", lambda x: '"' + x.group(1).replace("\"", "\\\"") + '"', value)

def clean_whitespace(code: str) -> str:
  clean_code = ""
  is_str = False
  for i,char in enumerate(code):
    if char == "\"" and code[i-1] != "\\":
      is_str = not is_str
    if not is_str and re.findall(r"\s", char):
      pass
    else:
      clean_code += char

  return clean_code
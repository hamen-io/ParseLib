import re

from parselib.lib.common import Validate,clean_whitespace

class BaseType:
  def __init__(self):
    self.value = ""
    self.real = None

  def __str__(self, **kwargs) -> str:
    return self.value

class Tokens:
  class String(BaseType):
    def __init__(self, raw_value: str):
      assert Validate.string(raw_value)

      self.value = raw_value[1:-1]
      self.real = self.value

    def lowercase(self) -> str:
      return self.real.lower()

    def uppercase(self) -> str:
      return self.real.upper()
    
    def trim(self, __chars: str = None) -> str:
      return self.real.strip()

    def __str__(self, **kwargs) -> str:
      quo = "\"" if kwargs.get("string_quotes") != False else ""
      return quo + self.real + quo

  class Number(BaseType):
    def __init__(self, raw_value: str):
      assert Validate.number(raw_value)
      raw_value = raw_value.strip()

      self.value = raw_value
      self.real = float(self.value)
      if self.real.is_integer():
        self.real = int(self.real)

  class Boolean(BaseType):
    def __init__(self, raw_value: str):
      assert Validate.boolean(raw_value)
      raw_value = raw_value.strip()

      self.value = raw_value
      self.real = True if raw_value == "true" else False

  class Null(BaseType):
    def __init__(self, raw_value: str):
      assert Validate.null(raw_value)
      raw_value = raw_value.strip()

      self.value = raw_value
      self.real = None

  class Array(BaseType):
    def __init__(self, raw_value: str):
      assert Validate.array(raw_value)
      raw_value = raw_value.strip()

      self.value = raw_value[1:-1]
      self.real = self.__parse(self.value)

    def __parse(self, raw_value: str) -> list:
      array = [""]

      raw_value = clean_whitespace(raw_value)

      is_str = False
      level_brace = 0
      level_bracket = 0
      level_square = 0
      for i,char in enumerate(raw_value):
        if char == "\"" and raw_value[i-1] != "\\": is_str = not is_str
        level = level_brace + level_bracket + level_square

        if not is_str and char == "," and level == 0:
          array.append("")
          continue
        elif not is_str:
          if char == "{": level_brace += 1
          if char == "}": level_brace -= 1
          if char == "[": level_square += 1
          if char == "]": level_square -= 1
          if char == "(": level_bracket += 1
          if char == ")": level_bracket -= 1

        array[-1] += char

      array = [Tokens.tokenize_value(x.strip()) for x in array]

      return array
    
    def __str__(self, **kwargs) -> str:
      return "[" + ", ".join([x.__str__() for x in self.real]) + "]"

  class Object(BaseType):
    def __init__(self, raw_value: str):
      assert Validate.object(raw_value)
      raw_value = raw_value.strip()

      self.value: str = raw_value[1:-1]
      self.real: dict = self.__parse(self.value)

    def get(self, value: str) -> BaseType | None:
      for key in self.real:
        key: Tokens.String
        if key.real == value:
          return self.real[key]

    def __parse(self, raw_value: str) -> dict:
      entry_groups = [""]
      obj = dict()

      raw_value = clean_whitespace(raw_value)
      is_str = False
      level_brace = 0
      level_bracket = 0
      level_square = 0
      is_key = True
      for i,char in enumerate(raw_value):
        if char == "\"" and raw_value[i-1] != "\\": is_str = not is_str
        level = level_brace + level_bracket + level_square

        if not is_str and char == "," and level == 0 and is_key:
          entry_groups.append("")
          is_key = False
          continue

        elif not is_str:
          if char == "{": level_brace += 1
          if char == "}": level_brace -= 1
          if char == "[": level_square += 1
          if char == "]": level_square -= 1
          if char == "(": level_bracket += 1
          if char == ")": level_bracket -= 1

        if level == 0 and not is_str and char == ":":
          is_key = True

        entry_groups[-1] += char

      for term in entry_groups:
        assert term.strip(), "Blank term; perhaps you dangled a comma?"

        is_str = False
        key = value = None
        for i,char in enumerate(term):
          if char == "\"" and term[i-1] != "\\": is_str = not is_str
          if not is_str and char == ":":
            key = term[:i]
            value = term[i+1:]
            break

        assert Validate.string(key), "Keys must be strings!"
        value = Tokens.tokenize_value(value)
        key = Tokens.String(key)

        obj[key] = value

      return obj

    def __str__(self, *, pretty: bool = True, tab_size: int = 2, kv_space: str = " ", quote_keys: bool = True, **kwargs) -> str:
      nl = "\n" if pretty else ""
      tab = " " * tab_size if pretty else ""
      qt = "\"" if quote_keys else ""

      return f"{{{nl}{tab}" + f",{nl}{tab}".join([f"{qt}{k.__str__(string_quotes = False)}{qt}:{kv_space}{v.__str__(string_quotes = True)}" for k,v in self.real.items()]) + f"{nl}}}"

  def tokenize_value(value: str) -> BaseType:
    """
    Infers the correct token of `value`, then returns an instance of said token
    """

    if Validate.string(value):
      return Tokens.String(value)
    elif Validate.number(value):
      return Tokens.Number(value)
    elif Validate.array(value):
      return Tokens.Array(value)
    elif Validate.object(value):
      return Tokens.Object(value)
    elif Validate.boolean(value):
      return Tokens.Boolean(value)
    elif Validate.null(value):
      return Tokens.Null(value)
    else:
      raise SyntaxError("Unknown Value: " + value)
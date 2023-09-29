import re

import parselib.lib.types as types
import parselib.lib.common as common

class JSONParser:
  def __init__(self, *, code: str = None, file: str = None, __ALLOW_SINGLE_QUOTE_STRINGS__: bool = False, __ALLOW_SINGLE_LINE_COMMENTS__: bool = False, __ALLOW_MULTI_LINE_COMMENTS__: bool = False, __ALLOW_MULTI_LINE_STRINGS__: bool = False):
    assert (code and not file) or (not code and file), "`code` or `file` parameter must be given; not both; not none."

    self.__ALLOW_MULTI_LINE_COMMENTS__ = __ALLOW_MULTI_LINE_COMMENTS__
    self.__ALLOW_SINGLE_QUOTE_STRINGS__ = __ALLOW_SINGLE_QUOTE_STRINGS__
    self.__ALLOW_MULTI_LINE_STRINGS__ = __ALLOW_MULTI_LINE_STRINGS__
    self.__ALLOW_SINGLE_LINE_COMMENTS__ = __ALLOW_SINGLE_LINE_COMMENTS__

    self.code = code
    if file:
      with open(file, "r") as f:
        self.code = f.read()

    if self.__ALLOW_MULTI_LINE_COMMENTS__:
      self.code = re.sub(r"\/\*[\s\S]*\*\/", "", self.code)

    if self.__ALLOW_SINGLE_LINE_COMMENTS__:
      self.code = re.sub(r"\/\/.*", "", self.code)

    if self.__ALLOW_SINGLE_QUOTE_STRINGS__:
      self.code = common.squo_to_dquo(self.code)

  def parse(self) -> types.Tokens.Array or types.Tokens.Object:
    if types.Validate.object(self.code):
      return types.Tokens.Object(self.code)

    elif types.Validate.array(self.code):
      return types.Tokens.Array(self.code)

    else:
      raise SyntaxError("Wrapping type must be an object or array")
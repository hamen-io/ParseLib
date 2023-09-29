import parselib

json = parselib.json.JSONParser(code = """

{
  "test": [null, [[1e+2]]]
}

""", __ALLOW_SINGLE_QUOTE_STRINGS__=True).parse()

print(json.get("test"))
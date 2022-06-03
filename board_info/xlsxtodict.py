import pandas

ss = pandas.read_excel("./board.xlsx", sheet_name="spaces")
ws = ss.to_dict("records")
print(ws)

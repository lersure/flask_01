from flask import jsonify


def querysetToJson(sets=None):
    allValues = []
    if sets is None:
        return None
    for s in sets:
        jsonValue = {"ID": s.dataSets_id, "config": s.configToJson}
        allValues.append(jsonValue)
    return allValues


# {'configs': ["{'wqz':123,'qaz':'qqq'}", "{'3453':123,'qaz':'ttt'}", "{'45':787,'89':'45'}"], 'dm': 1, 'id': '123245'}
# {'configs': ["{'wqz':123,'qaz':'qqq'}"], 'dm': 1, 'id': '654321'}

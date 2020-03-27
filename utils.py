def db2dict(data):
    result = []
    key = ['slug', 'text', 'status', 'createdAt']
    for one in data:
        tmp = dict(zip(key, one))
        result.append(tmp)
    return result
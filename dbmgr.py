import redis


host = 'localhost'

port = 6379

redis = redis.StrictRedis(host=host, port=port, db=1)


def init(schema):

    redis.set('SCHEMA', repr(schema))


def isExists(key):

    for rec in redis.keys():

        if rec.decode('ascii') == 'SCHEMA': pass

        elif rec.decode('ascii') == key: return True

    return False;


def add(key, attrs):

    if isExists(key): return False

    else:

        schema = eval(redis.get('SCHEMA').decode('ascii'))

        record = {}

        for i, s in enumerate(schema): record[s[0]] = attrs[i]

        redis.set(str(key), str(record))

        return True


def delete(key):

    if not isExists(key): return False

    elif key == 'SCHEMA': return False

    else:

        redis.delete(key)

        return True


def getSchema():

    return eval(redis.get('SCHEMA').decode('ascii'))


def getRecords():

    schema = eval(redis.get('SCHEMA').decode('ascii'))

    collect = []

    for rec in redis.keys():

        if rec.decode('ascii') == 'SCHEMA': pass

        else:

            record = eval(redis.get(rec).decode('ascii'))

            collect.append(record)


    return collect

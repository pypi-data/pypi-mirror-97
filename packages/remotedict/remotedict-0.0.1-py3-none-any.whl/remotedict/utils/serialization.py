import joblib
import io


def serialize(data):

    with io.BytesIO() as b:
        joblib.dump({'data': data}, b, compress=("lz4", 1))
        b.seek(0)
        result = b.read()

    return result


def unserialize(b):
    with io.BytesIO(b) as b:
        b.seek(0)
        data = joblib.load(b)['data']

    return data

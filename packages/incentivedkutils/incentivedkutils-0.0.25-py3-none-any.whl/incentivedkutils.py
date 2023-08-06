def remove_dict_keys(dict, list_of_keys):
    ### removes list of keys from a dict ###
    for key in list_of_keys:
        dict.pop(key)
    return dict


def flatten_list(list):
    ### Flattens a list of lists ###
    return [item for sublist in list for item in sublist]


def dict_to_tuples(dict):
    ### converts dict to tuple of sorted tuples ###
    return tuple(sorted(tuple((k, v) for k, v in dict.items())))


def to_pickle(obj, pickle_filename):
    ### saves obj to pickle file ###
    import pickle
    with open(pickle_filename, 'wb') as f:
        pickle.dump(obj, f)


def from_pickle(pickle_filename):
    ### inports obj from pickle file ###
    import pickle
    with open(pickle_filename, 'rb') as f:
        obj = pickle.load(f)
    return obj



def load_csv(file, delimiter=','):
    ### loads csv file ###
    import csv
    with open(file, 'r') as infile:
        load_parms = [{k: empty_to_None(v) for k, v in dict(obs).items()} for obs in
                      csv.DictReader(infile, delimiter=delimiter)]
    return load_parms


def load_csv_utf8(file, delimiter=','):
    ### loads utf-8 encoded csv file ###
    import csv
    with open(file, 'r', encoding='utf-8-sig') as infile:
        load_parms = [{k: empty_to_None(v) for k, v in dict(obs).items()} for obs in
                      csv.DictReader(infile, delimiter=delimiter)]
    return load_parms


def f2(x):
    ### converts number to string number with comma seperator and 2 decimals ###
    return '{:,.2f}'.format(x)


def f4(x):
    ### converts number to string number with comma seperator and 4 decimals ###
    return '{:,.4f}'.format(x)


def f0(x):
    ### converts number to string number with comma seperator and 0 decimals ###
    return '{:,.0f}'.format(x)


def prt(obj):
    ### prints obj in a nicer fashion than print ###
    if type(obj) is list:
        for obs in obj:
            print(obs)
    elif type(obj) is dict:
        for key, val in sorted(obj.items()):
            print(key, '\t:\t', val)
    else:
        print(obj)


def print_df(df):
    ### prints dataframe ###
    from tabulate import tabulate
    print(tabulate(df, headers='keys', tablefmt='grid'))


def print_namespace(args):
    ### prints namespace ###
    for d in vars(args):
        print(d, '\t', vars(args)[d])


class dict_to_namespace(object):
    ### converts dict to namespace ###
    def __init__(self, adict):
        self.__dict__.update(adict)


def print_time(txt='', st=0):
    ### prints txt plus time in seconds elapsed since st ###
    from datetime import datetime
    seconds = datetime.utcnow().timestamp() - st
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    print(txt, '{:1d}:{:02d}:{:05.2f}'.format(int(h), int(m), s))


class Namespace():
    ### Defines empty namespace ###
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

def timer():
    from functools import wraps
    from datetime import datetime
    def dec_outer(fn):
        @wraps(fn)
        def dec_inner(*args, **kwargs):
            st = datetime.utcnow().timestamp()
            response = fn(*args, **kwargs)
            print(f'{fn.__name__} ran in {f2(datetime.utcnow().timestamp() - st)} seconds')
            return response
        return dec_inner
    return dec_outer


def cache(reload=True):
    from functools import wraps
    def dec_outer(fn):
        @wraps(fn)
        def dec_inner(*args, **kwargs):
            if reload:
                response = fn(*args, **kwargs)
                to_pickle(response, 'cache.pkl')
            else:
                import os.path
                if os.path.isfile('cache.pkl'):
                    response = from_pickle('cache.pkl')
                else:
                    response = fn(*args, **kwargs)
                    to_pickle(response, 'cache.pkl')
            return response
        return dec_inner
    return dec_outer


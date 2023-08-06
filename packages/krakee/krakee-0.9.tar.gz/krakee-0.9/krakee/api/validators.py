
def assert_list (elem, param_name):
    assert (type(elem) == list), "{} parameter should be a list, type={} found".format(param_name, type(elem))

def asset_pair (krakee, pair):
    if type(pair) == list:
        for pair in pair:
            assert (pair in list(krakee.asset_pairs().columns)), "Invalid pair: {}".format(pair)
    else:
        assert (pair in list(krakee.asset_pairs().columns)), "Invalid pair: {}".format(pair)

def assert_interval (interval, intervals):
    assert (interval in intervals), "{} interval not in {}".format(interval, list(intervals.keys()))
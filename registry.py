site_list = []


def register(cls):
    site_list.append(cls())
    return cls

def print_tags(tags):
    return ';'.join(['%s=%s' % (k, v) for k, v in tags.items()])


def print_str(label):
    return label if label else ''

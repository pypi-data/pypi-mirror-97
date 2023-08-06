from pkg_resources import get_distribution
from email import message_from_string

def get_version(metadata):
    for item, data in metadata:
        if item.upper() == 'VERSION':
            return data
    return 'UNKNOWN'

if __name__ == '__main__':
    module = 'PyExecTime'
    try:
        pkgInfo = get_distribution(module).get_metadata('PKG-INFO')
    except:
        pkgInfo = get_distribution(module).get_metadata('METADATA')
    msg = message_from_string(pkgInfo)
    items = msg.items()
    version_info = get_version(items)
    print('{0} - {1}'.format(module, version_info))
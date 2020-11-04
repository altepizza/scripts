import requests
from getpass import getpass

print('This script will look for bookmarks linked to not existing folders and move them into a folder called "TEMP RECOVERY"')
URL = input(
    'Please enter your basic url in this exact format https://your.cloud.com: ')
USER = input('Please enter your username: ')
PASSWORD = getpass('Please enter your nextcloud password or app password: ')
print('I am not responsible if anything goes wrong. You can inspect the code yourself.')
start = input('Continue? [y/n]: ')
if start.lower() != 'y':
    quit()


def create_recovery_folder(name='TEMP RECOVERY'):
    print('Creating target folder')
    payload = {'title': name, 'parent_folder': -1}
    response = requests.post(
        URL + '/index.php/apps/bookmarks/public/rest/v2/folder', auth=(USER, PASSWORD), data=payload).json()
    return response['item']['id']


def get_bookmarks():
    print('Getting bookmarks...')
    response = requests.get(
        URL + '/index.php/apps/bookmarks/public/rest/v2/bookmark?page=-1', auth=(USER, PASSWORD)).json()
    bookmarks = response['data']
    print('Found {0} bookmarks'.format(len(bookmarks)))
    return bookmarks


def get_folder_ids():
    print('Getting folders...')
    folder_ids = []

    response = requests.get(
        URL + '/index.php/apps/bookmarks/public/rest/v2/folder', auth=(USER, PASSWORD)).json()
    root_folders = response['data']
    for folder in root_folders:
        folder_ids = folder_ids + _get_ids(folder)
    return set(folder_ids)


def move_orphans(folder_id, orphan_bookmarks):
    print('Moving orphans...')
    for orphan in orphan_bookmarks:
        response = requests.post(
            URL + '/index.php/apps/bookmarks/public/rest/v2/folder/{0}/bookmarks/{1}'.format(folder_id, orphan['id']), auth=(USER, PASSWORD)).json()
        if response['status'] == 'success':
            print(
                'Moved {0} - {1}'.format(orphan['title'], orphan['url']))


def _get_ids(child):
    tmp_ids = []
    if child['children']:
        for folder in child['children']:
            tmp_ids = tmp_ids + _get_ids(folder)
    tmp_ids.append(child['id'])
    return tmp_ids


bookmarks = get_bookmarks()
folders = get_folder_ids()
folders.add(-1)
bookmarks = [b for b in bookmarks if set(b['folders']) - folders]
print('Orphaned {0} bookmarks'.format(len(bookmarks)))
your_sure = input('Continue? [y/n]: ')
if your_sure.lower() != 'y':
    quit()
print('This might take a while....')
recovery_folder_id = create_recovery_folder()
move_orphans(recovery_folder_id, bookmarks)
print('Done')

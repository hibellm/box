# coding: utf-8

from __future__ import print_function, unicode_literals
import os
from boxsdk import Client
from boxsdk.exception import BoxAPIException
from boxsdk.object.collaboration import CollaborationRole
<<<<<<< HEAD
# from auth import authenticate
=======
from auth import authenticate

#DEVELOPMENT TOKEN
devtoken='xxx'
>>>>>>> master

# DEVELOPMENT TOKEN
devtoken='N8cfPlhPz1I55WxjvzK24l62jZX4araV'

from boxsdk import DevelopmentClient
client = DevelopmentClient()

user = client.user().get()
print('The current user ID is {0}'.format(user.id))


def run_user_example(client):

    # 'me' is a handy value to get info on the current authenticated user.
    me = client.user(user_id='me').get(fields=['login'])
    print('About the user:')
    print(f"Name : {user['name']}")
    print(f"Email: {user['login']}")
    print(f"Phone: {user['phone']}")

run_user_example(client)


def run_folder_examples(client):
    root_folder = client.folder(folder_id='0').get()
    print('The root folder is owned by: {0}'.format(root_folder.owned_by['login']))

    items = root_folder.get_items(limit=100, offset=0)
    print('These are the first 100 items in the root folder:')
    for item in items:
        print(f"Folder: {item.name} [{item._description}]")

    return items

x = run_folder_examples(client)


def get_folderinfo(client, folder_id):

    folder_info = client.folder(folder_id).get()

    print('Folder info:')
    print(f"         id: {folder_info['id']}")
    print(f"       name: {folder_info['name']}")
    print(f"description: {folder_info['description']}")
    print(f" created by: {folder_info['created_by']._description} [{folder_info['created_at']}]")

    return folder_info


folder_info = get_folderinfo(client, '66753612692')


def get_fileinfo(client, file_id):

    file_items = client.folder(folder_id='66753612692').get_items()

    file_info = client.folder(file_id).get()

    print(f"Folder info:")
    print(f"         id: {file_info['id']}")
    print(f"       name: {file_info['name']}")
    print(f"description: {file_info['description']}")
    print(f" created by: {file_info['created_by']._description} [{file_info['created_at']} ]")

    return file_info


file_info = get_fileinfo(client, '66753612692')


def run_collab_examples(client):
    root_folder = client.folder(folder_id='0')
    collab_folder = root_folder.create_subfolder('collab folder')
    try:
        print(f"Folder {collab_folder.get()['name']} created")
        collaboration = collab_folder.add_collaborator('someone@example.com', CollaborationRole.VIEWER)
        print("Created a collaboration")
        try:
            modified_collaboration = collaboration.update_info(role=CollaborationRole.EDITOR)
            print(f"Modified a collaboration: {modified_collaboration.role}")
        finally:
            collaboration.delete()
            print('Deleted a collaboration')
    finally:
        # Clean up
        print(f"Delete folder collab folder succeeded: {collab_folder.delete()}")



def create_folder(client, foldername=None, root_folder_id='0', ):
    root_folder = client.folder(root_folder_id)

    try:
        newfolder = root_folder.create_subfolder(foldername)
        print(f"Folder created : {newfolder.get()['name']}")
    except Exception as e:
        print('Something went wrong with creating a folder...')
        print('Folder probably already exists...getting folder list ')
        run_folder_examples(client)

create_folder(client, 'marcustest')



def rename_folder(client):
    root_folder = client.folder(folder_id='0')
    foo = root_folder.create_subfolder('foo')
    try:
        print(f"Folder {foo.get()['name']} created")

        bar = foo.rename('bar')
        print(f"Renamed to {bar.get()['name']}")
    finally:
        print(f"Delete folder bar succeeded: {foo.delete()}")

rename_folder(client)



def get_folder_shared_link(client):
    root_folder = client.folder(folder_id='0')
    collab_folder = root_folder.create_subfolder('shared link folder')
    try:
        print(f"Folder {collab_folder.get().name} created")

        shared_link = collab_folder.get_shared_link()
        print(f"Got shared link: {shared_link}")
    finally:
        print(f"Delete folder collab folder succeeded: {collab_folder.delete()}")


def upload_file(client):
    root_folder = client.folder(folder_id='0')
    file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'file.txt')
    a_file = root_folder.upload(file_path, file_name='i-am-a-file.txt')
    try:
        print(f"{a_file.get()['name']} uploaded: ")
    finally:
        print(f"Delete i-am-a-file.txt succeeded: {a_file.delete()}")


def upload_accelerator(client):
    root_folder = client.folder(folder_id='0')
    file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'file.txt')
    a_file = root_folder.upload(file_path, file_name='i-am-a-file.txt', upload_using_accelerator=True)
    try:
        print('{0} uploaded via Accelerator: '.format(a_file.get()['name']))
        file_v2_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'file_v2.txt')
        a_file = a_file.update_contents(file_v2_path, upload_using_accelerator=True)
        print('{0} updated via Accelerator: '.format(a_file.get()['name']))
    finally:
        print('Delete i-am-a-file.txt succeeded: {0}'.format(a_file.delete()))


def rename_file(client):
    root_folder = client.folder(folder_id='0')
    file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'file.txt')
    foo = root_folder.upload(file_path, file_name='foo.txt')
    try:
        print('{0} uploaded '.format(foo.get()['name']))
        bar = foo.rename('bar.txt')
        print('Rename succeeded: {0}'.format(bool(bar)))
    finally:
        foo.delete()


def update_file(client):
    root_folder = client.folder(folder_id='0')
    file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'file.txt')
    file_v1 = root_folder.upload(file_path, file_name='file_v1.txt')
    try:
        # print 'File content after upload: {}'.format(file_v1.content())
        file_v2_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'file_v2.txt')
        file_v2 = file_v1.update_contents(file_v2_path)
        # print 'File content after update: {}'.format(file_v2.content())
    finally:
        file_v1.delete()


def search_files(client):
    search_results = client.search().query(
        'i-am-a-file.txt',
        limit=2,
        offset=0,
        ancestor_folders=[client.folder(folder_id='0')],
        file_extensions=['txt'],
    )
    for item in search_results:
        item_with_name = item.get(fields=['name'])
        print('matching item: ' + item_with_name.id)
    else:
        print('no matching items')


def copy_item(client):
    root_folder = client.folder(folder_id='0')
    file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'file.txt')
    a_file = root_folder.upload(file_path, file_name='a file.txt')
    try:
        subfolder1 = root_folder.create_subfolder('copy_sub')
        try:
            a_file.copy(subfolder1)
            print(subfolder1.get_items(limit=10, offset=0))
            subfolder2 = root_folder.create_subfolder('copy_sub2')
            try:
                subfolder1.copy(subfolder2)
                print(subfolder2.get_items(limit=10, offset=0))
            finally:
                subfolder2.delete()
        finally:
            subfolder1.delete()
    finally:
        a_file.delete()


def move_item(client):
    root_folder = client.folder(folder_id='0')
    file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'file.txt')
    a_file = root_folder.upload(file_path, file_name='a file.txt')
    try:
        subfolder1 = root_folder.create_subfolder('move_sub')
        try:
            a_file.move(subfolder1)
            print(subfolder1.get_items(limit=10, offset=0))
            subfolder2 = root_folder.create_subfolder('move_sub2')
            try:
                subfolder1.move(subfolder2)
                print(subfolder2.get_items(limit=10, offset=0))
            finally:
                subfolder2.delete()
        finally:
            try:
                subfolder1.delete()
            except BoxAPIException:
                pass
    finally:
        try:
            a_file.delete()
        except BoxAPIException:
            pass


def get_events(client):
    print(client.events().get_events(limit=100, stream_position='now'))


def get_latest_stream_position(client):
    print(client.events().get_latest_stream_position())


def long_poll(client):
    print(client.events().long_poll())


def _delete_leftover_group(existing_groups, group_name):
    """
    delete group if it already exists
    """
    existing_group = next((g for g in existing_groups if g.name == group_name), None)
    if existing_group:
        existing_group.delete()


def run_groups_example(client):
    """
    Shows how to interact with 'Groups' in the Box API. How to:
    - Get info about all the Groups to which the current user belongs
    - Create a Group
    - Rename a Group
    - Add a member to the group
    - Remove a member from a group
    - Delete a Group
    """
    try:
        # First delete group if it already exists
        original_groups = client.groups()
        _delete_leftover_group(original_groups, 'box_sdk_demo_group')
        _delete_leftover_group(original_groups, 'renamed_box_sdk_demo_group')

        new_group = client.create_group('box_sdk_demo_group')
    except BoxAPIException as ex:
        if ex.status != 403:
            raise
        print('The authenticated user does not have permissions to manage groups. Skipping the test of this demo.')
        return

    print('New group:', new_group.name, new_group.id)

    new_group = new_group.update_info({'name': 'renamed_box_sdk_demo_group'})
    print("Group's new name:", new_group.name)

    me_dict = client.user().get(fields=['login'])
    me = client.user(user_id=me_dict['id'])
    group_membership = new_group.add_member(me, 'member')

    members = list(new_group.membership())

    print('The group has a membership of: ', len(members))
    print('The id of that membership: ', group_membership.object_id)

    group_membership.delete()
    print('After deleting that membership, the group has a membership of: ', len(list(new_group.membership())))

    new_group.delete()
    groups_after_deleting_demo = client.groups()
    has_been_deleted = not any(g.name == 'renamed_box_sdk_demo_group' for g in groups_after_deleting_demo)
    print('The new group has been deleted: ', has_been_deleted)


def run_metadata_example(client):
    root_folder = client.folder(folder_id='0')
    file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'file.txt')
    foo = root_folder.upload(file_path, file_name='foo.txt')
    print('{0} uploaded '.format(foo.get()['name']))
    try:
        metadata = foo.metadata()
        metadata.create({'foo': 'bar'})
        print('Created metadata: {0}'.format(metadata.get()))
        update = metadata.start_update()
        update.update('/foo', 'baz', 'bar')
        print('Updated metadata: {0}'.format(metadata.update(update)))
    finally:
        foo.delete()


def run_examples(oauth):

    client = Client(oauth)

    run_user_example(client)
    run_folder_examples(client)
    run_collab_examples(client)
    rename_folder(client)
    get_folder_shared_link(client)
    upload_file(client)
    rename_file(client)
    update_file(client)
    search_files(client)
    copy_item(client)
    move_item(client)
    get_events(client)
    get_latest_stream_position(client)
    # long_poll(client)

    # Enterprise accounts only
    run_groups_example(client)
    run_metadata_example(client)

    # Premium Apps only
    upload_accelerator(client)


def main():

    # Please notice that you need to put in your client id and client secret in demo/auth.py in order to make this work.
    oauth, _, _ = authenticate()
    run_examples(oauth)
    os._exit(0)

if __name__ == '__main__':
    main()

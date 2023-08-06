def parse_directory(dir_mount):
    mount_path, volume_info = dir_mount.split(':', 1)


def parse_project(project_mount):
    mount_path, project_info = project_mount.split(':', 1)
    workspace_name, project_name = project_info.split('/', 1)


def parse_dataset(dataset_mount):
    mount_path, dataset_info = dataset_mount.split(':', 1)
    dataset_info, snapshot_name = dataset_info.split('@', 1)
    workspace_name, dataset_name = dataset_info.split('/', 1)

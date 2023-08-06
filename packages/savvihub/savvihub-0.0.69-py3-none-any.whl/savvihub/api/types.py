import inspect
import typeguard
import typing
import typing_inspect


class AnnotatedObject:
    def __init__(self, d: dict):
        resolved_types = {}
        for cls in self.__class__.mro():
            annotations = getattr(cls, '__annotations__', None)
            if annotations is None:
                continue

            for k, type_ in annotations.items():
                if k in resolved_types:
                    continue

                v = d.get(k, None)
                resolved_types[k] = type_

                type_origin = typing_inspect.get_origin(type_)
                if inspect.isclass(type_) and issubclass(type_, AnnotatedObject):
                    v = type_(v)
                elif type_origin in [typing.List, list]:
                    t = typing_inspect.get_args(type_)[0]
                    for i, elem in enumerate(v):
                        if inspect.isclass(t) and issubclass(t, AnnotatedObject):
                            v[i] = t(elem)
                        else:
                            typeguard.check_type(k, elem, t)
                elif type_origin == typing.Union:
                    for t in typing_inspect.get_args(type_):
                        try:
                            if inspect.isclass(t) and issubclass(t, AnnotatedObject):
                                v = t(v)
                            else:
                                typeguard.check_type(k, v, t)
                            break
                        except (TypeError, AttributeError):
                            continue
                    else:
                        raise TypeError(f'Union type failed: {k}, {v}')
                else:
                    typeguard.check_type(k, v, type_)
                setattr(self, k, v)
        self.d = d

    def __str__(self):
        return f'[{self.__class__.__name__}] {self.d}'

    @property
    def dict(self):
        return self.d


class SavviHubWorkspace(AnnotatedObject):
    id: int
    name: str


class SavviHubUser(AnnotatedObject):
    id: int
    username: str
    name: str
    github_authorized: bool
    workspaces: typing.List[SavviHubWorkspace]


class SavviHubDatasetSource(AnnotatedObject):
    type: str
    bucket_name: typing.Optional[str]
    path: typing.Optional[str]


class SavviHubDataset(AnnotatedObject):
    id: int
    workspace: SavviHubWorkspace
    name: str
    volume_id: int
    source: SavviHubDatasetSource


class SavviHubDatasetInfo(AnnotatedObject):
    dataset_id: int
    snapshot_id: int
    sub_path: str
    dataset: SavviHubDataset


class SavviHubFileObject(AnnotatedObject):
    path: str

    size: int
    hash: str

    download_url: typing.Optional[typing.Dict]
    upload_url: typing.Optional[typing.Dict]

    is_dir: typing.Optional[bool]


class SavviHubKernelCluster(AnnotatedObject):
    name: str
    kubernetes_master_endpoint: typing.Optional[str]
    kubernetes_namespace: typing.Optional[str]
    status: str
    is_savvihub_managed: bool
    created_dt: str


class SavviHubKernelImage(AnnotatedObject):
    id: int
    image_url: str
    name: str
    processor_type: str


class SavviHubKernelResource(AnnotatedObject):
    id: int
    name: str
    description: typing.Optional[str]
    processor_type: str
    cpu_limit: float
    memory_limit: str


class SavviHubSnapshot(AnnotatedObject):
    id: int
    name: str
    size: int


class SavviHubProject(AnnotatedObject):
    id: int
    workspace_id: int
    name: str
    volume_id: int


class SavviHubProjectInfo(AnnotatedObject):
    project_id: int
    branch: str
    git_ref: str
    commit_message: str
    project: SavviHubProject


class SavviHubVolume(AnnotatedObject):
    id: int
    created_dt: str
    updated_dt: str
    role_type: str
    storage_id: typing.Optional[int]
    workspace_id: typing.Optional[int]
    snapshot_volume_id: typing.Optional[int]


class SavviHubVolumeInfo(AnnotatedObject):
    volume_id: int
    sub_path: str
    volume: SavviHubVolume


class SavviHubVolumeMount(AnnotatedObject):
    path: str
    mount_type: str
    read_only: bool
    size: int
    source_type: str
    project: typing.Optional[SavviHubProjectInfo]
    dataset: typing.Optional[SavviHubDatasetInfo]
    volume: typing.Optional[SavviHubVolumeInfo]
    snapshot: typing.Optional[SavviHubSnapshot]


class SavviHubVolumeMountInfo(AnnotatedObject):
    root_volume_size: int
    working_dir: str
    mounts: typing.List[SavviHubVolumeMount]


class SavviHubSourceCodeLink(AnnotatedObject):
    project: typing.Optional[SavviHubProject]


class SavviHubExperiment(AnnotatedObject):
    class KernelImage(AnnotatedObject):
        name: str
        image_url: str
        language: typing.Optional[str]

    class KernelResourceSpec(AnnotatedObject):
        name: str
        cpu_type: str
        cpu_limit: float
        cpu_guarantee: typing.Optional[float]
        memory_limit: str
        mem_guarantee: typing.Optional[str]
        gpu_type: str
        gpu_limit: int
        gpu_guarantee: typing.Optional[int]

    class GitDiffFile(AnnotatedObject):
        path: str
        size: int
        hash: str
        download_url: typing.Optional[typing.Dict]
        is_dir: typing.Optional[bool]

    id: int
    name: str
    created_dt: str
    updated_dt: str
    number: int
    message: str
    status: str
    slug: str
    tensorboard_log_dir: typing.Optional[str]
    kernel_image: KernelImage
    kernel_resource_spec: KernelResourceSpec
    env_vars: typing.Optional[typing.List]
    tensorboard: typing.Optional[str]
    histories: typing.Optional[typing.List]
    metrics: typing.Optional[typing.List]
    source_code_link: typing.Optional[typing.List[SavviHubSourceCodeLink]]
    start_command: str
    git_ref: str
    git_diff_file: typing.Optional[GitDiffFile]


class SavviHubExperimentLog(AnnotatedObject):
    container: str
    stream: str
    message: str
    timestamp: float


class SavviHubExperimentMetric(AnnotatedObject):
    step: int
    value: str
    timestamp: float


class SavviHubListResponse(AnnotatedObject):
    results: typing.List


class PaginatedMixin(AnnotatedObject):
    total: int
    startCursor: typing.Optional[str]
    endCursor: typing.Optional[str]
    results: typing.List


class SavviHubFileMetadata(AnnotatedObject):
    path: str

import abc
from dataclasses import dataclass
from typing import Optional

from yarl import URL

from .parsing_utils import LocalImage, RemoteImage

# storage


@dataclass(frozen=True)
class StorageProgressStart:
    src: URL
    dst: URL
    size: int


@dataclass(frozen=True)
class StorageProgressComplete:
    src: URL
    dst: URL
    size: int


@dataclass(frozen=True)
class StorageProgressStep:
    src: URL
    dst: URL
    current: int
    size: int


@dataclass(frozen=True)
class StorageProgressEnterDir:
    src: URL
    dst: URL


@dataclass(frozen=True)
class StorageProgressLeaveDir:
    src: URL
    dst: URL


@dataclass(frozen=True)
class StorageProgressFail:
    src: URL
    dst: URL
    message: str


@dataclass(frozen=True)
class StorageProgressDelete:
    uri: URL
    is_dir: bool


class AbstractFileProgress(abc.ABC):
    # design note:
    # dataclasses used instead of direct passing parameters
    # because a dataclass is forward-compatible
    # but adding a new parameter to callback method
    # effectively breaks all existing code

    @abc.abstractmethod
    def start(self, data: StorageProgressStart) -> None:
        pass  # pragma: no cover

    @abc.abstractmethod
    def complete(self, data: StorageProgressComplete) -> None:
        pass  # pragma: no cover

    @abc.abstractmethod
    def step(self, data: StorageProgressStep) -> None:
        pass  # pragma: no cover


class AbstractRecursiveFileProgress(AbstractFileProgress):
    @abc.abstractmethod
    def enter(self, data: StorageProgressEnterDir) -> None:
        pass  # pragma: no cover

    @abc.abstractmethod
    def leave(self, data: StorageProgressLeaveDir) -> None:
        pass  # pragma: no cover

    @abc.abstractmethod
    def fail(self, data: StorageProgressFail) -> None:
        pass  # pragma: no cover


class AbstractDeleteProgress(abc.ABC):
    @abc.abstractmethod
    def delete(self, data: StorageProgressDelete) -> None:
        pass  # pragma: no cover


# Next class for typing only (wrapped with queue_calls version of above classes)


class _AsyncAbstractFileProgress(abc.ABC):
    @abc.abstractmethod
    async def start(self, data: StorageProgressStart) -> None:
        pass  # pragma: no cover

    @abc.abstractmethod
    async def complete(self, data: StorageProgressComplete) -> None:
        pass  # pragma: no cover

    @abc.abstractmethod
    async def step(self, data: StorageProgressStep) -> None:
        pass  # pragma: no cover


class _AsyncAbstractRecursiveFileProgress(_AsyncAbstractFileProgress):
    @abc.abstractmethod
    async def enter(self, data: StorageProgressEnterDir) -> None:
        pass  # pragma: no cover

    @abc.abstractmethod
    async def leave(self, data: StorageProgressLeaveDir) -> None:
        pass  # pragma: no cover

    @abc.abstractmethod
    async def fail(self, data: StorageProgressFail) -> None:
        pass  # pragma: no cover


class _AsyncAbstractDeleteProgress(abc.ABC):
    @abc.abstractmethod
    async def delete(self, data: StorageProgressDelete) -> None:
        pass  # pragma: no cover


# image


@dataclass(frozen=True)
class ImageProgressPull:
    src: RemoteImage
    dst: LocalImage


@dataclass(frozen=True)
class ImageProgressPush:
    src: LocalImage
    dst: RemoteImage


@dataclass(frozen=True)
class ImageProgressSave:
    job: str
    dst: RemoteImage


@dataclass(frozen=True)
class ImageProgressStep:
    message: str
    layer_id: str
    status: str
    current: Optional[float]
    total: Optional[float]


@dataclass(frozen=True)
class ImageCommitStarted:
    job_id: str
    target_image: RemoteImage


@dataclass(frozen=True)
class ImageCommitFinished:
    job_id: str


class AbstractDockerImageProgress(abc.ABC):
    @abc.abstractmethod
    def pull(self, data: ImageProgressPull) -> None:
        pass  # pragma: no cover

    @abc.abstractmethod
    def push(self, data: ImageProgressPush) -> None:
        pass  # pragma: no cover

    @abc.abstractmethod
    def step(self, data: ImageProgressStep) -> None:
        pass  # pragma: no cover

    @abc.abstractmethod
    def save(self, data: ImageProgressSave) -> None:
        pass  # pragma: no cover

    @abc.abstractmethod
    def commit_started(self, data: ImageCommitStarted) -> None:
        pass  # pragma: no cover

    @abc.abstractmethod
    def commit_finished(self, data: ImageCommitFinished) -> None:
        pass  # pragma: no cover

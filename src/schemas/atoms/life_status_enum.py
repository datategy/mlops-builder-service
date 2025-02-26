from enum import StrEnum, auto
from typing import Literal


class LifeStatus(StrEnum):
    """
    ```mermaid
    ---
    title: Life status
    ---
    stateDiagram
        [*] --> Pending
        Pending --> Building
        Building --> Build_and_deploy_failed
        Build_and_deploy_failed --> [*]
        Building --> Build_and_deploy_cancelled
        Build_and_deploy_cancelled --> [*]
        Building --> Build_and_deploy_succeeded
        Build_and_deploy_succeeded --> Pod_ready
        Pod_ready --> Pod_unreachable
        Pod_unreachable --> Pod_ready
        Pod_unreachable --> Deleted
        Pod_ready --> Pod_stopped
        Pod_stopped --> Pod_ready
        Pod_stopped --> Deleted
        Pod_ready --> Deleted
    ```
    """

    PENDING = auto()
    """Nothing has happened yet."""
    BUILDING = auto()
    """Build is running."""
    BUILD_FAILED = auto()
    """Build failed."""
    BUILD_CANCELLED = auto()
    """Build was cancelled."""
    BUILD_SUCCEEDED = auto()
    """Build was successful and deployment will start soon."""
    DEPLOYING = auto()
    """Deploy is running."""
    DEPLOY_FAILED = auto()
    """Deploy failed."""
    DEPLOY_CANCELLED = auto()
    """Deploy was cancelled."""
    DEPLOY_SUCCEEDED = auto()
    """Deploy was successful but the pod cannot be reached yet."""
    POD_READY = auto()
    """Pod is ready and accepts traffic."""
    POD_UNREACHABLE = auto()
    """Pod was ready but is now unreachable."""
    POD_STOPPED = auto()
    """Pod was stopped and is no longer reachable."""
    DELETED = auto()
    """Deployment was deleted."""


type GitLabLifeStatuses = Literal[
    LifeStatus.BUILDING,
    LifeStatus.BUILD_FAILED,
    LifeStatus.BUILD_CANCELLED,
    LifeStatus.BUILD_SUCCEEDED,
    LifeStatus.DEPLOYING,
    LifeStatus.DEPLOY_FAILED,
    LifeStatus.DEPLOY_CANCELLED,
    LifeStatus.DEPLOY_SUCCEEDED,
]

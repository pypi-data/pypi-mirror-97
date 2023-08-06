from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Optional

from scomconfig import SCOMCommand, SetSoftwareSwitch


@dataclass
class SCOMConfig:
    MPW: Optional[str] = None
    commands: Iterable[SCOMCommand] = field(default_factory=list)

    def __call__(self, command):
        self.commands.append(command)


c = SCOMConfig()
c(SetSoftwareSwitch('0123', '1'))

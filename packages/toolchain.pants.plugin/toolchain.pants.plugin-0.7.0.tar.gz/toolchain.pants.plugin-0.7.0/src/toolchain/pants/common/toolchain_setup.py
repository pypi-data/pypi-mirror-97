# Copyright © 2020 Toolchain Labs, Inc. All rights reserved.
#
# Toolchain Labs, Inc. CONFIDENTIAL
#
# This file includes unpublished proprietary source code of Toolchain Labs, Inc.
# The copyright notice above does not evidence any actual or intended publication of such source code.
# Disclosure of this source code or any related proprietary information is strictly prohibited without
# the express written permission of Toolchain Labs, Inc.

from typing import Optional

from pants.engine.rules import SubsystemRule
from pants.option.subsystem import Subsystem


class ToolchainSetupError(Exception):
    """Raised if the toolchain settings are not properly configured."""


class ToolchainSetup(Subsystem):
    options_scope = "toolchain-setup"
    help = """Setup specific to the Toolchain codebase."""

    @classmethod
    def register_options(cls, register) -> None:
        register("--repo", type=str, help="Repo name", default=None)

    def safe_get_repo_name(self) -> Optional[str]:
        return self.options.repo or None

    def get_repo_name(self) -> str:
        repo = self.safe_get_repo_name()
        if not repo:
            raise ToolchainSetupError("Repo must be set under toolchain-setup.repo.")
        return repo


def get_rules():
    return [SubsystemRule(ToolchainSetup)]

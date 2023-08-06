# Copyright © 2020 Toolchain Labs, Inc. All rights reserved.
#
# Toolchain Labs, Inc. CONFIDENTIAL
#
# This file includes unpublished proprietary source code of Toolchain Labs, Inc.
# The copyright notice above does not evidence any actual or intended publication of such source code.
# Disclosure of this source code or any related proprietary information is strictly prohibited without
# the express written permission of Toolchain Labs, Inc.

from typing import Dict

from pants.version import VERSION as PANTS_VERSION

from toolchain.pants.version import VERSION as TOOLCHAIN_VERSION


def get_common_request_headers() -> Dict[str, str]:
    return {"User-Agent": f"pants/v{PANTS_VERSION} toolchain/v{TOOLCHAIN_VERSION}"}

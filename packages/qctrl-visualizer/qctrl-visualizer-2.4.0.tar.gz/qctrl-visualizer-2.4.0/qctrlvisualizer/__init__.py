# Copyright 2020 Q-CTRL Pty Ltd & Q-CTRL Inc. All rights reserved.
#
# Licensed under the Q-CTRL Terms of service (the "License"). Unauthorized
# copying or use of this file, via any medium, is strictly prohibited.
# Proprietary and confidential. You may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#     https://q-ctrl.com/terms
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS. See the
# License for the specific language.

"""
Top-level package for the Q-CTRL Visualizer.

The public API of this package consists only of the objects exposed through this top-level package.
Direct access to sub-modules is not officially supported, so may be affected by
backwards-incompatible changes without notice.
"""
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from .bloch import (
    display_bloch_sphere,
    display_bloch_sphere_qutrit,
    display_two_qubit_visualization,
    print_bloch_sphere_data,
    print_bloch_sphere_data_qutrit,
)
from .controls import (
    plot_controls,
    plot_sequences,
    plot_smooth_controls,
)
from .discriminators import (
    plot_discriminator,
    plot_xdata,
)
from .filter_functions import plot_filter_functions
from .style import get_qctrl_style

# Note that, in the public version of this package, the Bloch sphere functions are simply stubs that
# print error messages. With that in mind, we exclude those functions from __all__, indicating that
# they should typically not be used by public users. A convenient side effect is that the functions
# are excluded from the generated reference documentation.
__all__ = [
    "get_qctrl_style",
    "plot_controls",
    "plot_discriminator",
    "plot_filter_functions",
    "plot_sequences",
    "plot_smooth_controls",
    "plot_xdata",
]

__version__ = "2.4.0"

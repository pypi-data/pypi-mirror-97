#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Define the CDKata main entry logic."""
from __future__ import annotations

from . import __version__

import fire


class CDKata:
    """Define the CDKata CLI object."""

    def __init__(self, **kwargs) -> None:
        """Initialize the CDKata CLI.

        This entrypoint is primarily for use with the CLI.

        """
        pass

    def __repr__(self) -> str:
        """Provide the representation for the CDKata object.

        Returns:
            str: The string representation of the CDKata object.

        """
        return "<CDKata>"

    @property
    def version(self) -> str:
        """Display the CDKata module version.

        Returns:
            str: The CDKata Python module version.

        """
        return __version__


def main() -> None:
    """Define the main entry method for the CLI."""
    # Run CDKata via the pipeline object for easy CLI access.
    fire.Fire(CDKata)


if __name__ == "__main__":
    main()

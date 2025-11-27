"""
Skeleton for clip template application.
"""

class ClipTemplate:
    """Placeholder template implementation."""

    def __init__(self, name: str) -> None:
        self.name = name

    def apply(self, input_path: str, output_path: str) -> str:
        """
        Apply template styles.
        Currently identity – future releases will add branded overlays.
        """
        return input_path

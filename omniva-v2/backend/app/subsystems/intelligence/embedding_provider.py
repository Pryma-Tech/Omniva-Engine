"""
Placeholder embedding provider (deterministic vector generator).
"""

import hashlib
import random
from typing import List


class EmbeddingProvider:
    """Stable pseudo-embedding generator until real models are plugged in."""

    def embed_text(self, text: str) -> List[float]:
        digest = hashlib.sha256(text.encode()).hexdigest()
        random.seed(int(digest[:8], 16))
        return [random.random() for _ in range(64)]

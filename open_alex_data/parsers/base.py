from abc import ABC, abstractmethod
from typing import Any


class BaseParser(ABC):
    """Base class for parsing OpenAlex API responses."""

    @abstractmethod
    def parse(self, data: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
        """Parse data from API response.

        Parameters
        ----------
        data : List[Dict[str, Any]]
            List of data dictionaries from API response

        Returns
        -------
        Dict[str, List[Dict[str, Any]]]
            Dictionary of tables and their rows
        """

    @staticmethod
    def invert_abstract(inv_index: dict | None) -> str | None:
        """Invert OpenAlex abstract index.

        Parameters
        ----------
        inv_index : dict
            Inverted index of the abstract.

        Returns
        -------
        str | None
            Inverted abstract or None if input is None.
        """
        if inv_index is None:
            return None
        try:
            l_inv_new = {}
            for w, pos in inv_index.items():
                if not pos:
                    continue
                l_inv_new[w] = pos
            l_inv = [(w, p) for w, pos in l_inv_new.items() for p in pos if pos]
        except TypeError:
            print(l_inv_new)
            return None
        return " ".join(map(lambda x: x[0], sorted(l_inv, key=lambda x: x[1])))

"""Repository pattern implementation for warehouse storage."""
from abc import ABC, abstractmethod
from typing import Dict, Optional
from varasto import Varasto


class WarehouseData:  # pylint: disable=too-few-public-methods
    """Data class representing a warehouse entity."""

    def __init__(self, warehouse_id: int, nimi: str, varasto: Varasto):
        self.id = warehouse_id
        self.nimi = nimi
        self.varasto = varasto


class WarehouseRepository(ABC):
    """Abstract base class for warehouse repository."""

    @abstractmethod
    def get_all(self) -> Dict[int, WarehouseData]:
        """Get all warehouses.

        Returns:
            Dictionary mapping warehouse IDs to WarehouseData objects.
        """

    @abstractmethod
    def get_by_id(self, warehouse_id: int) -> Optional[WarehouseData]:
        """Get a warehouse by its ID.

        Args:
            warehouse_id: The ID of the warehouse to retrieve.

        Returns:
            WarehouseData object if found, None otherwise.
        """

    @abstractmethod
    def create(self, nimi: str, tilavuus: float,
               alku_saldo: float) -> WarehouseData:
        """Create a new warehouse.

        Args:
            nimi: Name of the warehouse.
            tilavuus: Capacity of the warehouse.
            alku_saldo: Initial balance of the warehouse.

        Returns:
            The created WarehouseData object.
        """

    @abstractmethod
    def update(self, warehouse_id: int, nimi: str,
               tilavuus: float, alku_saldo: float) -> bool:
        """Update an existing warehouse.

        Args:
            warehouse_id: The ID of the warehouse to update.
            nimi: New name of the warehouse.
            tilavuus: New capacity of the warehouse.
            alku_saldo: New balance of the warehouse.

        Returns:
            True if update was successful, False otherwise.
        """

    @abstractmethod
    def delete(self, warehouse_id: int) -> bool:
        """Delete a warehouse.

        Args:
            warehouse_id: The ID of the warehouse to delete.

        Returns:
            True if deletion was successful, False otherwise.
        """

    @abstractmethod
    def add_to_warehouse(self, warehouse_id: int, maara: float) -> bool:
        """Add content to a warehouse.

        Args:
            warehouse_id: The ID of the warehouse.
            maara: Amount to add.

        Returns:
            True if addition was successful, False otherwise.
        """


class InMemoryWarehouseRepository(WarehouseRepository):
    """In-memory implementation of warehouse repository."""

    def __init__(self):
        self._warehouses: Dict[int, WarehouseData] = {}
        self._next_id: int = 1

    def get_all(self) -> Dict[int, WarehouseData]:
        """Get all warehouses."""
        return self._warehouses.copy()

    def get_by_id(self, warehouse_id: int) -> Optional[WarehouseData]:
        """Get a warehouse by its ID."""
        return self._warehouses.get(warehouse_id)

    def create(self, nimi: str, tilavuus: float,
               alku_saldo: float) -> WarehouseData:
        """Create a new warehouse."""
        warehouse_data = WarehouseData(
            warehouse_id=self._next_id,
            nimi=nimi,
            varasto=Varasto(tilavuus, alku_saldo)
        )
        self._warehouses[self._next_id] = warehouse_data
        self._next_id += 1
        return warehouse_data

    def update(self, warehouse_id: int, nimi: str,
               tilavuus: float, alku_saldo: float) -> bool:
        """Update an existing warehouse."""
        if warehouse_id not in self._warehouses:
            return False

        self._warehouses[warehouse_id].nimi = nimi
        self._warehouses[warehouse_id].varasto = Varasto(tilavuus, alku_saldo)
        return True

    def delete(self, warehouse_id: int) -> bool:
        """Delete a warehouse."""
        if warehouse_id in self._warehouses:
            del self._warehouses[warehouse_id]
            return True
        return False

    def add_to_warehouse(self, warehouse_id: int, maara: float) -> bool:
        """Add content to a warehouse."""
        warehouse = self.get_by_id(warehouse_id)
        if warehouse is None:
            return False

        warehouse.varasto.lisaa_varastoon(maara)
        return True

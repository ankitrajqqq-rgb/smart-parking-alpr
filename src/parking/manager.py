class ParkingManager:
    def __init__(self, total_slots):
        self.total_slots = total_slots
        self.available_slots = list(range(1, total_slots + 1))
        self.occupied = {}  # plate → slot

    def assign_slot(self, plate):
        # If already inside → return same slot
        if plate in self.occupied:
            return self.occupied[plate]

        # If parking full
        if not self.available_slots:
            return None

        # Assign first available slot
        slot = self.available_slots.pop(0)
        self.occupied[plate] = slot
        return slot

    def release_slot(self, plate):
        if plate in self.occupied:
            slot = self.occupied.pop(plate)
            self.available_slots.append(slot)
            self.available_slots.sort()
            return slot
        return None

    def get_status(self):
        return {
            "total": self.total_slots,
            "available": len(self.available_slots),
            "occupied": len(self.occupied)
        }
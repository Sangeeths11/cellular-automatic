import heapq


class PriorityItem[T]:
    def __init__(self, item: T, priority: float):
        self.item = item
        self.priority = priority

    def __lt__(self, other):
        return self.priority < other.priority

    def __eq__(self, other):
        return self.priority == other.priority

    def __gt__(self, other):
        return self.priority > other.priority

    def get_item(self) -> T:
        return self.item

class PathfindingQueue[T]:
    def __init__(self):
        self._queue: list[PriorityItem[T]] = []
        self._items: set[T] = set()

    def __contains__(self, item: T) -> bool:
        return item in self._items

    def __len__(self):
        return len(self._queue)

    def mark_visited(self, item: T):
        self._items.add(item)

    def pop(self) -> T:
        item = heapq.heappop(self._queue)
        return item.get_item()

    def push(self, item: T, priority: float):
        self._items.add(item)
        heapq.heappush(self._queue, PriorityItem(item, priority))
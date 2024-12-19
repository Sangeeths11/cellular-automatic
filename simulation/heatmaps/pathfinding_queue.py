import heapq


class PriorityItem[T]:
    """
    Wrapper class for items in the PathfindingQueue, holds a float for priority and an item of generic type T
    """
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
    """
    Priority queue for pathfinding algorithms, which also keeps track of visited items
    """
    def __init__(self):
        self._queue: list[PriorityItem[T]] = []
        self._items: set[T] = set()

    def __contains__(self, item: T) -> bool:
        return item in self._items

    def __len__(self):
        return len(self._queue)

    def mark_visited(self, item: T) -> None:
        """
        Marks an item as visited
        :param item: item which should be marked as visited
        """
        self._items.add(item)

    def pop(self) -> T:
        """
        Pops the item with the lowest priority from the queue
        :return: popped item
        """
        item = heapq.heappop(self._queue)
        return item.get_item()

    def push(self, item: T, priority: float) -> None:
        """
        Pushes an item to the queue with the given priority and marks it as visited
        :param item: the item to push
        :param priority: the priority of the item, lowest gets popped first
        """
        self._items.add(item)
        heapq.heappush(self._queue, PriorityItem(item, priority))

    def is_empty(self) -> bool:
        """
        :return: return true if the queue is empty
        """
        return len(self._queue) == 0
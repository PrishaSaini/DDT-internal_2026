"""A queue of listings waiting for the admin to check.

First in, firstt out, so longest wait is dealt with first.
"""
from collections import deque


class ReviewQueue:
    """Queue of items waiting to be checked, oldest first"""

    def __init__(self, items=()):
        pending = [item for item in items if item.status == "pending"]
        # Oldest first. Items with no date go last.
        pending.sort(key=lambda item: (
            item.date_created is None, item.date_created))
        self._queue = deque(pending)

    def __len__(self):
        """How many items are waiting."""
        return len(self._queue)

    def is_empty(self):
        """True if nothing is waiting."""
        return not self._queue

    def peek(self):
        """Look at the next item without removing it."""
        return self._queue[0] if self._queue else None

    def take(self):
        """Take the next item out of the queue."""
        return self._queue.popleft() if self._queue else None

    def add(self, item):
        """Add an item to the back."""
        self._queue.append(item)

    def return_to_front(self, item):
        """Put an item back at the front"""
        self._queue.appendleft(item)


if __name__ == "__main__":
    # Check the queue really is first in, first out.
    from datetime import datetime
    from models.records import Item

    def fake(item_id, status, day):
        """Make a pretend item for testing"""
        return Item(
            item_id=item_id,
            name=f"Item {item_id}",
            category="Uniform",
            size="M",
            condition="Good",
            price=1.0,
            listing_type="Sale",
            status=status,
            seller_id=1,
            photo_path="",
            reject_reason="",
            drop_time="",
            date_created=datetime(
                2026,
                1,
                day))
    # Out of order on purpose, with two items tah need no checking.
    queue = ReviewQueue([fake(1, "pending", 3), fake(2, "active", 1),
                         fake(3, "pending", 1), fake(4, "rejected", 2),
                         fake(5, "pending", 2)])
    assert len(queue) == 3, "only pending items belong in the queue"
    assert queue.peek().item_id == 3, "oldest pending item must come first"
    assert queue.take().item_id == 3
    assert queue.take().item_id == 5
    assert len(queue) == 1

    # Putting one back should place it first.
    queue.return_to_front(fake(9, "pending", 1))
    assert queue.peek().item_id == 9

    # Adding goes to the back.
    queue.add(fake(10, "pending", 1))
    assert queue.take().item_id == 9
    assert queue.take().item_id == 1
    assert queue.take().item_id == 10

    # An empty queue must not crash.
    assert queue.is_empty() and queue.peek() is None and queue.take() is None
    assert len(ReviewQueue([])) == 0

    print("review queue self-check OK")

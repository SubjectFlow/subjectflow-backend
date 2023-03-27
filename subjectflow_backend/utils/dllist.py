class DLListNode:
    def __init__(self, data=None):
        self.data = data
        self.next = None
        self.prev = None


class DLList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def append(self, data):
        newNode = DLListNode(data)
        if self.head == None:
            self.head = newNode
            self.tail = newNode
        else:
            newNode.prev = self.tail
            self.tail.next = newNode
            self.tail = newNode

        self.size += 1
        return newNode

    def remove(self, node: DLListNode):
        if node.prev is not None:
            if node.next is not None:
                node.prev.next = node.next
                node.next.prev = node.prev
            else:
                self.tail = node.prev
                node.prev.next = None
        elif node.next is not None:
            node.next.prev = None
            self.head = node.next
        else:
            self.tail = None
            self.head = None

        self.size -= 1

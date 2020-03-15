from PIL import Image
import numpy as np
from heap import Heap

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, end, img):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    img.putpixel(end_node.position, (0, 0, 255))

    for position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:  # Adjacent squares
        img.putpixel(position, (255, 255, 0))

    heap = Heap()
    closed_list = {}

    # Add the start node
    heap.add(start_node)

    pop_counter = 0

    # Loop until you find the end
    while len(heap.l) > 0:
        current_node = heap.pop()
        pop_counter += 1
        img.putpixel(current_node.position, (0, 0, 255))

        if counter == 100000:
            img.show()
            counter = 0

        closed_list[current_node.position] = current_node

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current)
                current = current.parent

            return path[::-1] # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:
            # Child is on the closed list
            if child.position in closed_list:
                continue

            # Create the f, g, and h values
            red_value = maze[child.position[0]][child.position[1]][0]
            if red_value == 0:
                red_value = 1

            child.f = 255 - red_value

            # Child is already in the open list
            for open_node in heap.l:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            heap.add(child)


def main():
    print("Best First Search / heap")
    print("-" * 10)

    img_path = input("Enter the name of the image: ")
    img = Image.open(img_path)

    print(img)

    arr = np.array(img)

    print("Best First Search")
    print("-" * 10)

    x = int(input("Start node x: "))
    y = int(input("Start node y: "))

    start = (x, y)

    x = int(input("End node x: "))
    y = int(input("End node y: "))

    end = (x, y)

    path = astar(arr, start, end, img)

    for pixel in path:
        img.putpixel(pixel.position, (0, 255, 0))

    print(path)
    img.show()

if __name__ == '__main__':
    main()
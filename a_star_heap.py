from PIL import Image
import numpy as np
from heap import Heap
import time


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


def astar(maze, start, end, img, start_time):
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
    open_list = {}
    closed_list = {}

    # Add the start node
    heap.add(start_node)
    open_list[start_node.position] = [start_node]
    # to keep the max value of the heap
    max_item = 1

    pop_counter = 0

    # Loop until you find the end
    while len(heap.l) > 0:
        current_node = heap.pop()
        print(maze[current_node.position[0]][current_node.position[1]][0])
        if current_node.position in open_list:
            min_node = open_list[current_node.position][0]
            for node in open_list[current_node.position]:
                if node.f < min_node.f:
                    min_node = node
            open_list[current_node.position].remove(min_node)

            if len(open_list[current_node.position]) == 0:
                del open_list[current_node.position]

        closed_list[current_node.position] = current_node

        pop_counter += 1

        img.putpixel(current_node.position, (0, 0, 255))

        if pop_counter % 50000 == 0:
            img.show()
            print("-" * 10)
            get_exe_time(start_time)
            print("Pop counter: {}".format(pop_counter))

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current)
                current = current.parent

            return path[::-1], max_item  # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:  # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (
                    len(maze[len(maze) - 1]) - 1) or node_position[1] < 0:
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

            child.g = current_node.g + (255 - red_value)
            child.h = max(abs(child.position[0] - end_node.position[0]), abs(child.position[1] - end_node.position[1]))
            child.f = child.g + child.h

            # Child is already in the open list
            # for open_node in heap.l:
            #    if child == open_node and child.g > open_node.g:
            #        continue

            # if child.position in open_list and child.g > open_list[child.position].g:
            #    continue

            if child.position in open_list and len(open_list[child.position]) > 0:
                min_node = open_list[child.position][0]
                for node in open_list[child.position]:
                    if node.g < min_node.g:
                        min_node = node
                if child.g > min_node.g:
                    continue

            # Add the child to the open list
            heap.add(child)
            if child.position in open_list:
                open_list[child.position].append(child)
            else:
                open_list[child.position] = [child]
        # print(open_list)

        if len(heap.l) > max_item:
            max_item = len(heap.l)


def get_exe_time(start_time):
    end_time = time.time() - start_time

    total_hour = int(end_time // 3600)
    end_time = end_time % 3600

    total_min = int(end_time // 60)
    end_time = end_time % 60

    total_sec = int(end_time)

    print("Searching time: {}:{}:{}".format(total_hour, total_min, total_sec))


def main():
    print("A* / heap")
    print("-" * 10)

    img_path = input("Enter the name of the image: ")
    img = Image.open(img_path)

    print(img)

    arr = np.array(img)

    x = int(input("Start node x: "))
    y = int(input("Start node y: "))

    start = (x, y)
    print(start)

    x = int(input("End node x: "))
    y = int(input("End node y: "))

    end = (x, y)
    print(end)

    start_time = time.time()
    path, max_item = astar(arr, start, end, img, start_time)

    print("Search is completed.")
    get_exe_time(start_time)
    print([node.position for node in path])
    print("Max number of item in the heap during the execution: {}".format(max_item))

    for pixel in path:
        img.putpixel(pixel.position, (0, 255, 0))

    img.show()


if __name__ == '__main__':
    main()

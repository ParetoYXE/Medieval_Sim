import random, math
import networkx as nx_graph
from npc import NPC

class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = self.generate_map()




    def find_shortest_path(self, start_x, start_y, end_x, end_y):
        # Implement your pathfinding algorithm here (e.g., A*)
        # Return a list of (x, y) tuples representing the shortest path
        # For simplicity, here's a dummy pathfinding algorithm that just returns a straight line
        path = [(start_x, start_y)]
        if start_x < end_x:
            path.extend([(x, start_y) for x in range(start_x + 1, end_x + 1)])
        else:
            path.extend([(x, start_y) for x in range(start_x - 1, end_x - 1, -1)])
        if start_y < end_y:
            path.extend([(end_x, y) for y in range(start_y + 1, end_y + 1)])
        else:
            path.extend([(end_x, y) for y in range(start_y - 1, end_y - 1, -1)])
        return path

    def generate_map(self):
        # Create an empty map
        new_map = []
        for _ in range(self.height):
            new_map.append([0] * self.width)

        # Generate spawn points
        num_spawns = random.randint(200,300)  # Adjust the number of spawn points as needed
        spawn_points = [(random.randint(0, self.width - 1), random.randint(0, self.height - 1)) for _ in range(num_spawns)]

        # Create clusters of trees around each spawn point
        for x, y in spawn_points:
            cluster_size = random.randint(100, 150)  # Adjust the cluster size as needed
            for _ in range(cluster_size):
                angle = random.uniform(0, 2 * math.pi)
                radius = random.uniform(1, 5)
                nx = max(0, min(self.width - 1, int(x + math.cos(angle) * radius)))
                ny = max(0, min(self.height - 1, int(y + math.sin(angle) * radius)))
                new_map[ny][nx] = 1


        # Generate towns
        num_towns = random.randint(20, 30)  # Adjust the number of towns as needed
        towns = []
        for _ in range(num_towns):
            town_x = random.randint(0, self.width - 4)
            town_y = random.randint(0, self.height - 4)
            cluster_size = random.randint(5, 10)  # Adjust the cluster size of buildings in the town
            for _ in range(cluster_size):
                tx = max(0, min(self.width - 1, random.randint(town_x - 5, town_x + 5)))
                ty = max(0, min(self.height - 1, random.randint(town_y - 5, town_y + 5)))
                if not (new_map[ty][tx] == 3 or new_map[ty][tx + 1] == 3 or new_map[ty][tx - 1] == 3 or
                        new_map[ty + 1][tx + 1] == 3 or new_map[ty + 1][tx - 1] == 3 or new_map[ty + 1][tx] == 4):
                    # Render town as several tiles
                    new_map[ty][tx] = 3  # Use a different value for town buildings
                    new_map[ty][tx + 1] = 3
                    new_map[ty][tx - 1] = 3
                    new_map[ty + 1][tx + 1] = 3
                    new_map[ty + 1][tx - 1] = 3
                    new_map[ty + 1][tx] = 4
                    towns.append((tx, ty))

        # Generate roads using Minimum Spanning Tree (MST) algorithm
        graph = nx_graph.Graph()
        for i, (x, y) in enumerate(towns):
            graph.add_node(i, pos=(x, y))
        for i in range(len(towns)):
            for j in range(i + 1, len(towns)):
                distance = math.sqrt((towns[i][0] - towns[j][0]) ** 2 + (towns[i][1] - towns[j][1]) ** 2)
                graph.add_edge(i, j, weight=distance)
        mst = nx_graph.minimum_spanning_tree(graph)
        for edge in mst.edges():
            start_x, start_y = towns[edge[0]]
            end_x, end_y = towns[edge[1]]
            path = self.find_shortest_path(start_x, start_y, end_x, end_y)
            for x, y in path:
                if new_map[y][x] != 3 and new_map[y][x] != 4:  # Do not overwrite town or road tiles
                    new_map[y][x] = 5  # Use a different value for roads
        

        # Generate rivers
        num_rivers = random.randint(10, 30)  # Adjust the number of rivers as needed
        for _ in range(num_rivers):
            start_x = random.randint(0, self.width - 1)
            start_y = random.randint(0, self.height - 1)
            direction = random.uniform(0, 2 * math.pi)
            for _ in range(100):
                new_map[start_y][start_x] = 2  # Use a different value for rivers
                dx = math.cos(direction)
                dy = math.sin(direction)
                start_x = max(0, min(self.width - 1, int(start_x + dx)))
                start_y = max(0, min(self.height - 1, int(start_y + dy)))
                if random.random() < 0.1:  # Change direction occasionally
                    direction += random.uniform(-math.pi / 2, math.pi / 2)

        return new_map

    def generate_random_npcs(self,map_width, map_height, num_npcs):
        npcs = []
        for _ in range(num_npcs):
            x = random.randint(0, map_width - 1)
            y = random.randint(0, map_height - 1)
            npc_type = random.choice(['bandit', 'villager', 'merchant'])  # Example NPC types
            health = random.randint(50, 100)
            attack = random.randint(10, 20)
            defense = random.randint(5, 15)
            xp = random.randint(0, 50)
            npc = NPC(x, y, npc_type, health, attack, defense, xp)
            npcs.append(npc)
        return npcs
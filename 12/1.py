
class Robot:
    """
             +Y
             90 
             N
             ^
 -X 180 W  < * >  E  0  +X
             v
             S
            270
            -Y
    """
    # dirname => (dx, dy)
    directions_to_deltas = {
        'E': (1, 0),
        'N': (0, 1),
        'W': (-1, 0),
        'S': (0, -1)
    }
    degrees_to_directions = {
        0: 'E',
        90: 'N',
        180: 'W',
        270: 'S'
    }
    rotation_directions = {
        'R': -1,
        'L': 1
    }
    def __init__(self, instructions):
        self.instructions = instructions
        self.cur_degrees = 0
        self.x = 0
        self.y = 0

    def execute_command(self, cmd, val):
        if cmd in {'N', 'S', 'E', 'W'}:
            dx, dy = self.directions_to_deltas[cmd]
            self.x += dx * val
            self.y += dy * val
        elif cmd in {'R', 'L'}:
            self.cur_degrees += self.rotation_directions[cmd] * val
            self.cur_degrees %= 360
        elif cmd == 'F':
            cur_direction = self.degrees_to_directions[self.cur_degrees]
            dx, dy = self.directions_to_deltas[cur_direction]
            self.x += dx * val
            self.y += dy * val

    def run_to_completion(self):
        for cmd, val in self.instructions:
            self.execute_command(cmd, val)


def main():
    instructions = []
    with open("input.txt") as file:
        for line in file:
            instructions.append((line[:1], int(line[1:].strip())))
    robot = Robot(instructions)
    robot.run_to_completion()
    m_dist = abs(robot.x) + abs(robot.y)
    print(f"Coord: ({robot.x}, {robot.y}) Deg: {robot.cur_degrees} Man_Distance: {m_dist}") 

if __name__ == "__main__":
    main()

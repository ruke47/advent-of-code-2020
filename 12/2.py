
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
    def __init__(self, instructions):
        self.instructions = instructions
        self.x = 0
        self.y = 0
        self.wx = 10
        self.wy = 1

    def execute_command(self, cmd, val):
        if cmd in {'N', 'S', 'E', 'W'}:
            dx, dy = self.directions_to_deltas[cmd]
            self.wx += dx * val
            self.wy += dy * val
        elif cmd in {'L', 'R'}:
            normal_val = val if cmd == 'R' else (val * -1) % 360 
            if normal_val == 90:
                temp = self.wx
                self.wx = self.wy
                self.wy = -1 * temp
            elif normal_val == 180:
                self.wx *= -1 
                self.wy *= -1
            elif normal_val == 270:
                temp = self.wx
                self.wx = -1 * self.wy
                self.wy = temp
            else:
                raise ValueError("I don't know how to rotate {val} degrees!")
        elif cmd == 'F':
            self.x += val * self.wx
            self.y += val * self.wy 
        else:
            raise ValueError("Unrecognized command {cmd}")
        self.print_state(cmd,val)

    def run_to_completion(self):
        for cmd, val in self.instructions:
            self.execute_command(cmd, val)

    def print_state(self, cmd, val):
        print(f"After {cmd, val}\n  Pos: {self.x, self.y}\n  Way: {self.wx, self.wy}\n")

def main():
    instructions = []
    with open("input.txt") as file:
        for line in file:
            instructions.append((line[:1], int(line[1:].strip())))
    robot = Robot(instructions)
    robot.run_to_completion()
    m_dist = abs(robot.x) + abs(robot.y)
    print(f"Coord: ({robot.x}, {robot.y}) Man_Distance: {m_dist}") 

if __name__ == "__main__":
    main()

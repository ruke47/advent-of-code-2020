from math import ceil

with open("input.txt") as file:
    init_time = int(file.readline())
    busses = []
    for bus_str in file.readline().strip().split(","):
        if bus_str == "x":
            continue
        bus_num = int(bus_str)
        loop = ceil(init_time/bus_num)
        depart_time = loop * bus_num
        busses.append((bus_num, depart_time))
    busses.sort(key=lambda pair: pair[1])
    first_depart = busses[0] 

    print(f"Depart on bus {first_depart[0]} at {first_depart[1]} for {first_depart[0] * (first_depart[1] - init_time)}")


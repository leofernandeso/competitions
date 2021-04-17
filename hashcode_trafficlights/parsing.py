from collections import defaultdict, deque
from typing import Iterator, TextIO

def read_metadata(file_handle: TextIO) -> dict:
    mapped_metadata = map(int, file_handle.readline().split())
    return dict(
        zip(
            ['simulation_duration', 'num_intersections', 'num_streets', 'num_cars', 'bonus_points'],
            mapped_metadata
        )
    )

def read_streets(file_handle: TextIO, num_streets: int) -> Iterator[dict]:
    for _ in range(num_streets):
        street_info = file_handle.readline()
        street_info = street_info.split()
        street_info[0] = int(street_info[0])    # beggining intersection
        street_info[1] = int(street_info[1])    # ending intersection
        street_info[3] = int(street_info[3])    # time for crossing
        street_info = dict(zip(['begin', 'end', 'name', 'crossing_time'], street_info))
        street_info['id'] = f"{street_info['begin']}_{street_info['end']}"
        yield street_info

def read_cars(file_handle: TextIO, num_cars: int) -> Iterator[dict]:
    for i in range(num_cars):
        car_info = file_handle.readline()
        car_info = car_info.split()
        num_streets, path = int(car_info[0]), car_info[1:]
        complete_path = path.copy()
        path = deque(path)
        yield {
            'id': i, 'num_streets': num_streets, 'path': path, 'complete_path': complete_path
        }

def read_execution_plan(file_handle: TextIO) -> Iterator[dict]:
    num_intersections = int(file_handle.readline())
    schedule = defaultdict(list)
    for _ in range(num_intersections):
        intersection_id = int(file_handle.readline())
        num_streets_in_intersection = int(file_handle.readline())
        for _ in range(num_streets_in_intersection):
            street_name, green_time = file_handle.readline().split()
            green_time = int(green_time)
            schedule[intersection_id].append(
                (street_name, green_time)
            )
    return schedule

if __name__ == '__main__':
    
    # Reading simulation data
    example_filepath = "/home/leonardo/fun/competitions/hashcode_trafficlights/input/hashcode.in"
    fp = open(example_filepath, 'r')
    simulation_metadata = read_metadata(fp)
    streets = read_streets(fp, simulation_metadata['num_streets'])
    cars = read_cars(fp, simulation_metadata['num_cars'])
    fp.close()

    # Reading simulation execution schedule
    schedule_filepath = "/home/leonardo/fun/competitions/hashcode_trafficlights/input/example_schedule.in"
    fp = open(schedule_filepath, 'r')
    execution_plan = read_execution_plan(fp)
    fp.close()
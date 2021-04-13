import parsing
import utils
import copy
from city import City
from typing import Iterator
from collections import deque

class CitySimulation:
    def __init__(self, city: City, cars: Iterator[dict], schedule: dict, simulation_duration: int):
        self.simulation_duration = simulation_duration
        self.city = copy.copy(city)
        self.initialize_simulation()
        
    def initialize_simulation(self):
        self.timestep = 0
        for _, _, street_data in self.city.streets:
            street_data['traffic_light_state'] = False  # False: red, True: green
            street_data['cars_queue'] = deque()
        self.place_cars_in_initial_position(cars)
        self.assign_schedule_to_intersections(schedule)
        self.assign_schedule_to_streets()

    def place_cars_in_initial_position(self, cars: Iterator[dict]):
        for car in cars:
            for street_name in car['path']:
                street = self.city.get_street(street_name)
                street['cars_queue'].append(car)

    def assign_schedule_to_intersections(self, schedule: dict):
        for intersection_num, intersection_schedule in schedule.items():
            intersection = self.city.get_intersection(intersection_num)
            intersection['schedule'] = intersection_schedule

    def get_intersections_cycles(self):
        intersections_cycles = {}
        for intersection_num, intersection_schedule in self.city.intersections:
            intersection_schedule = intersection_schedule.get('schedule')
            if intersection_schedule:
                intersection_cycle = utils.schedule_to_cycle(intersection_schedule, self.simulation_duration)
            else:
                intersection_cycle = [None] * self.simulation_duration
            intersections_cycles[intersection_num] = intersection_cycle
        return intersections_cycles

    def assign_schedule_to_streets(self):
        intersections_cycles = self.get_intersections_cycles()
        print(intersections_cycles)
        pass

if __name__ == '__main__':

    example_filepath = "/home/leonardo/fun/competitions/hashcode_trafficlights/input/example.in"
    schedule_filepath = "/home/leonardo/fun/competitions/hashcode_trafficlights/input/example_schedule.in"

    # Reading simulation data
    fp_input = open(example_filepath, 'r')
    simulation_metadata = parsing.read_metadata(fp_input)
    streets = parsing.read_streets(fp_input, simulation_metadata['num_streets'])
    cars = parsing.read_cars(fp_input, simulation_metadata['num_cars'])

    # Reading simulation execution schedule
    schedule_filepath = "/home/leonardo/fun/competitions/hashcode_trafficlights/input/example_schedule.in"
    fp_schedule = open(schedule_filepath, 'r')
    schedule = parsing.read_execution_plan(fp_schedule)
    fp_schedule.close()

    # Building city with streets
    city = City(streets)
    assert city.num_intersections == simulation_metadata['num_intersections']
    assert city.num_streets == simulation_metadata['num_streets']

    # Building city scenario
    city_simulation = CitySimulation(city, cars, schedule, simulation_duration=simulation_metadata['simulation_duration'])

    fp_input.close()

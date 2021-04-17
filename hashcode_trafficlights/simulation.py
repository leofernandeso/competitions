import logging
import parsing
import utils
import copy
from city import City
from typing import Iterator
from collections import deque
from pprint import pprint

logging.basicConfig(filename='logfile.log', encoding='utf-8', level=logging.INFO)

class CitySimulation:
    def __init__(self, city: City, cars: Iterator[dict], schedule: dict, simulation_duration: int, bonus_points: int):
        self.simulation_duration = simulation_duration
        self.bonus_points = bonus_points
        self.city = copy.copy(city)
        self.initialize_simulation()

    @property
    def cars_state(self):
        cars_state_ = {}
        for _, _, street_data in self.city.streets:
            cars_state_.update({car['id']: car for car in street_data['cars_queue']})
        return cars_state_
    
    @property
    def traffic_light_cycles(self):
        return {
            num_intersection: intersection['cycle'] for num_intersection, intersection in self.city.intersections
        }

    def initialize_simulation(self) -> None:
        self.timestep = 0
        self.score = 0
        for _, _, street_data in self.city.streets:
            street_data['cars_queue'] = deque()
        self.place_cars_in_initial_position(cars)
        self.assign_cycle_to_intersections(schedule)

    def place_cars_in_initial_position(self, cars: Iterator[dict]) -> None:
        for car in cars:
            car_initial_street_name = car['path'].popleft()
            street = self.city.get_street(car_initial_street_name)
            street['cars_queue'].append(car)
            car['time_left_to_cross_current_street'] = 0
            car['current_street'] = car_initial_street_name

    def assign_cycle_to_intersections(self, schedule: dict) -> None:
        # Let's assign the raw schedule tuples first
        for intersection_num, intersection_schedule in schedule.items():
            intersection = self.city.get_intersection(intersection_num)
            intersection['schedule'] = intersection_schedule

        # Now, let's compute and assign the cycled schedules for each intersection
        for intersection_num, intersection_cycle in self.get_intersections_cycles().items():
            intersection = self.city.get_intersection(intersection_num)
            intersection['cycle'] = intersection_cycle
        
    def get_intersections_cycles(self) -> dict:
        intersections_cycles = {}
        for intersection_num, intersection_schedule in self.city.intersections:
            intersection_schedule = intersection_schedule.get('schedule')
            if intersection_schedule:
                intersection_cycle = utils.schedule_to_cycle(intersection_schedule, self.simulation_duration)
            else:
                intersection_cycle = [None] * self.simulation_duration
            intersections_cycles[intersection_num] = intersection_cycle
        return intersections_cycles

    def record_car_score(self, car: dict) -> None:
        time_remaining = self.simulation_duration - self.timestep
        self.score += time_remaining + self.bonus_points
        logging.info(f"Finished for car with ID '{car['id']}' - {time_remaining} seconds before the end of the simulation. Updated score: {self.score}")

    def move_car_to_next_street(self, car: dict) -> None:
        if len(car['path']) == 0:
            return self.record_car_score(car)
        car_next_street_name = car['path'].popleft()
        logging.info(f"Moving car {car['id']} from {car['current_street']} to {car_next_street_name}")
        next_street = self.city.get_street(car_next_street_name)
        car['time_left_to_cross_current_street'] = next_street['crossing_time']
        car['current_street'] = car_next_street_name
        next_street['cars_queue'].append(car)

    def set_street_green_light(self, street_name: str) -> None:
        street = self.city.get_street(street_name)
        if len(street['cars_queue']):
            first_waiting_car = street['cars_queue'][0]
            if first_waiting_car['time_left_to_cross_current_street'] == 0:
                first_waiting_car = street['cars_queue'].popleft()
                self.move_car_to_next_street(first_waiting_car)
        else:
            logging.info(f"No car waiting in the queue from street {street_name}. Proceeding.")

    def travel_cars(self) -> None:
        for _, _, street_data in self.city.streets:
            for car in street_data['cars_queue']:
                if car['time_left_to_cross_current_street'] > 0:
                    car['time_left_to_cross_current_street'] -= 1

    def step(self):

        logging.info(f"T = {self.timestep}:")

        if self.timestep == self.simulation_duration:
            log_str = f"Finished simulation. - Final score: {self.score}"
            logging.info(log_str)
            print(log_str)
            return self.score

        for intersection_num, intersection in self.city.intersections:
            next_green_street_name = intersection['cycle'][self.timestep]
            if next_green_street_name:
                self.set_street_green_light(next_green_street_name)
        self.travel_cars()
        self.timestep += 1
        
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
    city_simulation = CitySimulation(
        city,
        cars,
        schedule,
        simulation_duration=simulation_metadata['simulation_duration'],
        bonus_points=simulation_metadata['bonus_points']
    )

    fp_input.close()

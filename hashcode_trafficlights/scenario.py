import parsing
import copy
from city import City
from typing import Iterator
from collections import deque

class CityScenario:
    def __init__(self, city: City, cars: Iterator[dict]):
        self.city = copy.copy(city)
        self.initialize_scenario_variables()
        self.place_cars_in_initial_position(cars)
        
    def initialize_scenario_variables(self):
        self.timestep = 0
        for _, _, street_data in self.city.streets:
            street_data['traffic_light_state'] = False  # False: red, True: green
            street_data['cars_queue'] = deque()

    def place_cars_in_initial_position(self, cars: Iterator[dict]):
        for car in cars:
            for street_name in car['path']:
                street = self.city.get_edge(street_name)
                street['cars_queue'].append(car)

if __name__ == '__main__':

    example_filepath = "/home/leonardo/fun/kaggle/hashcode.in"
    fp = open(example_filepath, 'r')

    simulation_metadata = parsing.read_metadata(fp)
    streets = parsing.read_streets(fp, simulation_metadata['num_streets'])
    cars = parsing.read_cars(fp, simulation_metadata['num_cars'])

    # Building city with streets
    city = City(streets)
    assert city.num_intersections == simulation_metadata['num_intersections']
    assert city.num_streets == simulation_metadata['num_streets']

    # Building city scenario
    city_scenario = CityScenario(city, cars)

    fp.close()
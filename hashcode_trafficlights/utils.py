import itertools

def build_cycle_from_schedule(intersection_schedule: list[tuple]):
    cycle = []
    for street_name, green_duration in intersection_schedule:
        cycle += [street_name] * green_duration
    return cycle

def repeat_cycle_until_timestep(cycle: list, max_timestep: int):
    return list(itertools.islice(itertools.cycle(cycle), max_timestep))


def schedule_to_cycle(cycle_definition: list[tuple], timesteps: int):
    schedule_cycle = build_cycle_from_schedule(cycle_definition)
    intersection_cycle = repeat_cycle_until_timestep(schedule_cycle, timesteps)
    return intersection_cycle
    
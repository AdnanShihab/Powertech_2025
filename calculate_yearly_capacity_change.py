#




def calculate_yearly_capacity_change(year, previous_year):
    capacity_change = {}
    for component in initial_capacity.keys():
        capacity_change[component] = capacity_per_year[year][component] - capacity_per_year[previous_year][component]
    return capacity_change
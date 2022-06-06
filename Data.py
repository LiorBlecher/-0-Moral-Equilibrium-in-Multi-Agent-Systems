from statistics import mean


class Data:
    def __init__(self):
        self.utility_data = {}
        self.agent_data = {'Iteration': [], 'ID': [], 'Assignment': [], 'Utility': [], 'Moral Equilibrium': [],
                           'Base Line': [], 'Bound': []}
        self.neighbours_data = {'ID': [], 'neighbours': []}
        self.ME_agent_data = {'Iteration': [], 'Assignment': [], 'Utility': [], 'Moral Equilibrium': []}
        self.ME_neighbours_data = {'Iteration': [], 'ID': [], 'Assignment': [], 'Utility': [], 'Base Line': [],
                                   'Bound': []}
        self.global_utility_data = {'Iteration': [], 'Global Utility': []}
        self.any_time_data = {'Iteration': [], 'Best Global Utility': []}
        # ------------------------------------------helper for calculations:
        self.total_agents = 0
        self.helper = {'utility - start': [],
                       'utility - finish': [],
                       'neighbours utility - start': [],
                       'neighbours utility - finish': [],
                       'utility - highest global': [],
                       'neighbours utility - highest global': []}
        self.best_iteration = 0  # when global utility is max

    def set_neighbours_data(self, data):
        for agent_id in data.keys():
            self.neighbours_data['ID'].append(agent_id)
            self.neighbours_data['neighbours'].append(data[agent_id])
            self.total_agents = len(data) - 1

        # ---------------------------------------------------------------------update num agents for utility_data cols
        for agent_id in data.keys():
            self.utility_data[agent_id] = []

    def update_data(self, data):
        # 0 - id of ME agent
        # ME_neighbours:
        ME_neighbours = self.neighbours_data['neighbours'][0]
        # Iteration, ID, Assignment, Utility, Moral Equilibrium, baseLine, bound
        iteration = data[0]
        id = data[1]
        assignment = data[2]
        utility = data[3]
        moralEquilibrium = data[4]
        baseLine = data[5]
        bound = data[6]
        # ------------------------------------------------------------------------agent_data
        self.agent_data['Iteration'].append(iteration)
        self.agent_data['ID'].append(id)
        self.agent_data['Assignment'].append(assignment)
        self.agent_data['Utility'].append(utility)
        self.agent_data['Moral Equilibrium'].append(moralEquilibrium)
        self.agent_data['Base Line'].append(baseLine)
        self.agent_data['Bound'].append(bound)
        # ******************************************** helper:
        if iteration == 0:
            self.helper['utility - start'].append(utility)
        if iteration == 999:
            self.helper['utility - finish'].append(utility)

        # ------------------------------------------------------------------------utility_data
        self.utility_data[id].append(utility)
        # ------------------------------------------------------------------------ME_agent_data
        if id == 0:
            self.ME_agent_data['Iteration'].append(iteration)
            self.ME_agent_data['Assignment'].append(assignment)
            self.ME_agent_data['Utility'].append(utility)
            self.ME_agent_data['Moral Equilibrium'].append(moralEquilibrium)
        if id in ME_neighbours:
            self.ME_neighbours_data['Iteration'].append(iteration)
            self.ME_neighbours_data['ID'].append(id)
            self.ME_neighbours_data['Assignment'].append(assignment)
            self.ME_neighbours_data['Utility'].append(utility)
            self.ME_neighbours_data['Base Line'].append(baseLine)
            self.ME_neighbours_data['Bound'].append(bound)
            # ******************************************** helper:
            if iteration == 0:
                self.helper['neighbours utility - start'].append(utility)
            if iteration == 999:
                self.helper['neighbours utility - finish'].append(utility)
        # ------------------------------------------------------------------------global_utility_data
        if id == self.total_agents:
            self.global_utility_data['Iteration'].append(iteration)
            global_uti = 0
            for agent_id in range(self.total_agents):
                global_uti += self.utility_data[agent_id][-1]
            self.global_utility_data['Global Utility'].append(global_uti)
            if iteration == 0:
                self.any_time_data['Iteration'].append(iteration)
                self.any_time_data['Best Global Utility'].append(global_uti)
            # ------------------------------------------------------------------------any_time_data
            elif global_uti > max(self.any_time_data['Best Global Utility']):
                self.any_time_data['Iteration'].append(iteration)
                self.best_iteration = iteration
                self.any_time_data['Best Global Utility'].append(global_uti)

    def update_best_iteration_data(self):
        for agent_id in range(0, self.total_agents+1):
            agent_uti_per_iteration = self.utility_data[agent_id]
            uti = agent_uti_per_iteration[self.best_iteration]
            self.helper['utility - highest global'].append(uti)
            ME_neighbours = self.neighbours_data['neighbours'][0]
            if agent_id in ME_neighbours:
                self.helper['neighbours utility - highest global'].append(uti)



# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

class SimulationData:
    def __init__(self):
        self.criterion = ['special agent utility - start',
                          'special agent utility - finish',
                          'special agent utility - highest global',
                          'moral equilibrium - lowest',
                          'moral equilibrium - highest',
                          'moral equilibrium - finish',
                          'moral equilibrium - highest global',
                          'average utility - start',
                          'average utility - finish',
                          'average utility - highest global',
                          'special agent neighbors average utility - start',
                          'special agent neighbors average utility - finish',
                          'special agent neighbors average utility - highest global',
                          'global utility - finish',
                          'global utility - highest global']
        self.simulation_data = {'Criterion': self.criterion, 'Simple': [], 'Careful': [], 'Generous': [], 'Selfish': [],
                                'Random': [], 'Calculated': []}
        self.num_criterion = 15
        # ____________________________________________________________ME DATA
        self.moral_equilibrium = None
        self.utility = None

    def update_data(self, data, agent_type):
        best = data.best_iteration
        # --------------------------------------------------------------------special agent utility - start
        start = data.ME_agent_data['Utility'][0]
        self.simulation_data[agent_type].append(start)
        # --------------------------------------------------------------------special agent utility - finish
        finish = data.ME_agent_data['Utility'][-1]
        self.simulation_data[agent_type].append(finish)
        # --------------------------------------------------------------------special agent utility - highest global
        best_global = data.ME_agent_data['Utility'][best]
        self.simulation_data[agent_type].append(best_global)
        # --------------------------------------------------------------------moral equilibrium - lowest
        ME_lowest = min(data.ME_agent_data['Moral Equilibrium'])
        self.simulation_data[agent_type].append(ME_lowest)
        # --------------------------------------------------------------------moral equilibrium - highest
        ME_highest = max(data.ME_agent_data['Moral Equilibrium'])
        self.simulation_data[agent_type].append(ME_highest)
        # --------------------------------------------------------------------moral equilibrium - finish
        ME_finish = data.ME_agent_data['Moral Equilibrium'][-1]
        self.simulation_data[agent_type].append(ME_finish)
        # --------------------------------------------------------------------moral equilibrium - highest global
        ME_global = data.ME_agent_data['Moral Equilibrium'][best]
        self.simulation_data[agent_type].append(ME_global)
        # --------------------------------------------------------------------average utility - start
        avrg_utility_start = mean(data.helper['utility - start'])
        self.simulation_data[agent_type].append(avrg_utility_start)
        # --------------------------------------------------------------------average utility - finish
        avrg_utility_finish = mean(data.helper['utility - finish'])
        self.simulation_data[agent_type].append(avrg_utility_finish)
        # --------------------------------------------------------------------average utility - highest global
        avrg_utility_global = mean(data.helper['utility - highest global'])
        self.simulation_data[agent_type].append(avrg_utility_global)
        # ------------------------------------------------------------special agent neighbors average utility - start
        n_avrg_utility_start = mean(data.helper['neighbours utility - start'])
        self.simulation_data[agent_type].append(n_avrg_utility_start)
        # -----------------------------------------------------------special agents neighbors average utility - finish
        n_avrg_utility_finish = mean(data.helper['neighbours utility - finish'])
        self.simulation_data[agent_type].append(n_avrg_utility_finish)
        # ----------------------------------------------------special agents neighbors average utility - highest global
        n_avrg_utility_global = mean(data.helper['neighbours utility - highest global'])
        self.simulation_data[agent_type].append(n_avrg_utility_global)
        # ----------------------------------------------------------------------global utility - finish
        global_uti_finish = data.global_utility_data['Global Utility'][-1]
        self.simulation_data[agent_type].append(global_uti_finish)
        # ----------------------------------------------------------------------global utility - highest global
        global_uti_best = data.any_time_data['Best Global Utility'][-1]
        self.simulation_data[agent_type].append(global_uti_best)


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

class AllSimulationData:
    def __init__(self, sims_list):
        self.criterion = ['special agent utility - start',
                          'special agent utility - finish',
                          'special agent utility - highest global',
                          'moral equilibrium - lowest',
                          'moral equilibrium - highest',
                          'moral equilibrium - finish',
                          'moral equilibrium - highest global',
                          'average utility - start',
                          'average utility - finish',
                          'average utility - highest global',
                          'special agent neighbors average utility - start',
                          'special agent neighbors average utility - finish',
                          'special agent neighbors average utility - highest global',
                          'global utility - finish',
                          'global utility - highest global']
        self.simulations_list_data = {'Criterion': self.criterion, 'Simple': [], 'Careful': [], 'Generous': [],
                                      'Selfish': [], 'Random': [], 'Calculated': []}
        self.simulations_mean_data = {'Criterion': self.criterion, 'Simple': [], 'Careful': [], 'Generous': [],
                                      'Selfish': [], 'Random': [], 'Calculated': []}
        self.num_criterion = 15
        self.num_iterations = 1000
        self.all_simulations = sims_list
        self.agent_types = ['Simple', 'Careful', 'Generous', 'Selfish', 'Random', 'Calculated']


    def update_data(self):
        for agent_type in self.agent_types:
            for criterion in range(self.num_criterion):
                self.simulations_list_data[agent_type].append([])
                self.simulations_list_data[agent_type][criterion] = []
        for agent_type in self.agent_types:
            for data in self.all_simulations:
                for criterion in range(self.num_criterion):
                    cell = data.simulation_data[agent_type][criterion]
                    self.simulations_list_data[agent_type][criterion].append(cell)
        for agent_type in self.agent_types:
            for criterion in range(self.num_criterion):
                list_cell = self.simulations_list_data[agent_type][criterion]
                mean_cell = mean(list_cell)
                self.simulations_mean_data[agent_type].append(mean_cell)



class MEdata:
    def __init__(self):
        self.num_iterations = 100
        self.ME_uti_data = self.initiate_tables()


    def initiate_tables(self):
        ME_uti_data = {'Utility': [], 'Moral Equilibrium': []}
        for iteration in range(self.num_iterations):
            ME_uti_data['Utility'].append([])
            ME_uti_data['Utility'][iteration] = []
            ME_uti_data['Moral Equilibrium'].append([])
            ME_uti_data['Moral Equilibrium'][iteration] = []
        return ME_uti_data

    def update_data(self, data):
        for iteration in range(self.num_iterations):
            self.ME_uti_data['Utility'][iteration].append(data.ME_agent_data['Utility'][iteration])
            self.ME_uti_data['Moral Equilibrium'][iteration].append(data.ME_agent_data['Moral Equilibrium'][iteration])


    def mean_data(self):
        for iteration in range(self.num_iterations):
            list_cell_uti = self.ME_uti_data['Utility'][iteration]
            list_cell_ME = self.ME_uti_data['Moral Equilibrium'][iteration]
            mean_cell_uti = mean(list_cell_uti)
            mean_cell_ME = mean(list_cell_ME)
            self.ME_uti_data['Utility'][iteration] = mean_cell_uti
            self.ME_uti_data['Moral Equilibrium'][iteration] = mean_cell_ME











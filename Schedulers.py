from Agents.Agent import Agent
from Agents.MEagent import MEagent
from Agents.SMagent import SMagent
from Agents.AgentsTypes import SimpleAgent, CarefulAgent, GenerousAgent, SelfishAgent, RandomAgent, CalculatedAgent
from Messages.Message import Message
import numpy as np
import pandas as pd
from Simulation import Simulation
import openpyxl
from Data import Data, SimulationData, AllSimulationData, MEdata
import copy

final_iteration = 1000


def save_to_excel(id, data, name):
    utility_data = pd.DataFrame(data.utility_data)
    agent_data = pd.DataFrame(data.agent_data)
    neighbours_data = pd.DataFrame(data.neighbours_data)
    ME_agent_data = pd.DataFrame(data.ME_agent_data)
    ME_neighbours_data = pd.DataFrame(data.ME_neighbours_data)
    global_utility_data = pd.DataFrame(data.global_utility_data)
    any_time_data = pd.DataFrame(data.any_time_data)
    xlName = str(name) + str(id) + ".xlsx"
    xlwriter = pd.ExcelWriter(xlName)
    utility_data.to_excel(xlwriter, sheet_name='utilities')
    agent_data.to_excel(xlwriter, sheet_name='agents', index=False)
    neighbours_data.to_excel(xlwriter, sheet_name='neighbours', index=False)
    ME_agent_data.to_excel(xlwriter, sheet_name='ME agent', index=False)
    ME_neighbours_data.to_excel(xlwriter, sheet_name='ME neighbours', index=False)
    global_utility_data.to_excel(xlwriter, sheet_name='Global Utility', index=False)
    any_time_data.to_excel(xlwriter, sheet_name='Any Time', index=False)
    xlwriter.close()


def simulation_save_to_excel(id, sim):
    simulation_data = pd.DataFrame(sim.simulation_data)
    xlName = "Simulation" + str(id) + ".xlsx"
    xlwriter = pd.ExcelWriter(xlName)
    simulation_data.to_excel(xlwriter, sheet_name='simulation analysis', index=False)
    xlwriter.close()


def analysis_save_to_excel(sim):
    simulations_data = pd.DataFrame(sim.simulations_mean_data)
    xlName = "All_Simulation.xlsx"
    xlwriter = pd.ExcelWriter(xlName)
    simulations_data.to_excel(xlwriter, sheet_name='all simulations analysis', index=False)
    xlwriter.close()

def me_save_to_excel(simple, careful, generous, selfish, random, calculated):
    simple_ME_uti_data = pd.DataFrame(simple.ME_uti_data)
    careful_ME_uti_data = pd.DataFrame(careful.ME_uti_data)
    generous_ME_uti_data = pd.DataFrame(generous.ME_uti_data)
    selfish_ME_uti_data = pd.DataFrame(selfish.ME_uti_data)
    random_ME_uti_data = pd.DataFrame(random.ME_uti_data)
    calculated_ME_uti_data = pd.DataFrame(calculated.ME_uti_data)
    xlName = "All_Simulation_ME_vs_Utility.xlsx"
    xlwriter = pd.ExcelWriter(xlName)
    simple_ME_uti_data.to_excel(xlwriter, sheet_name='simple')
    careful_ME_uti_data.to_excel(xlwriter, sheet_name='careful')
    generous_ME_uti_data.to_excel(xlwriter, sheet_name='generous')
    selfish_ME_uti_data.to_excel(xlwriter, sheet_name='selfish')
    random_ME_uti_data.to_excel(xlwriter, sheet_name='random')
    calculated_ME_uti_data.to_excel(xlwriter, sheet_name='calculated')
    xlwriter.close()


# ----------------------------------------------------------------------------------------------------------
def neighbours2agent(neighbours, agents, agent_id):
    send = {}
    # neighbours_id is list of neighbours id
    neighbours_id = neighbours[agent_id]
    for neighbour_id in neighbours_id:
        # { key: id, value: neighbour}
        send[neighbour_id] = agents[neighbour_id]
    return send


def constraints2agent(constraints, agent_id):
    return constraints[agent_id]


def get_agent(agents, agent_id):
    return agents[agent_id]


# ----------------------------------------------------------------------------------------------------------
def SimulationSimple_run(id, simulation_data, me_uti_data, simple, agents, neighbours, constraints):
    data = Data()  # save data here
    agents[0] = simple  # replace with special agent
    data.set_neighbours_data(neighbours)  # update data - save connections
    for agent_id in agents.keys():
        # for every agent - initiate
        a_neighbours = neighbours2agent(neighbours, agents, agent_id)
        a_constraints = constraints2agent(constraints, agent_id)
        agent = get_agent(agents, agent_id)
        agent.initiate(a_neighbours, a_constraints)
    # start running the algorithm
    i = 0
    while i < final_iteration:
        up = False
        for agent_id in agents.keys():
            agent = get_agent(agents, agent_id)
            agent.listen()
        for agent_id in agents.keys():
            agent = get_agent(agents, agent_id)
            agent.reply()
            if agent.phase == 4:
                data.update_data(agent.get_data())  # save data here
                up = True
        if up:
            i = i + 1
    data.update_best_iteration_data()
    me_uti_data.update_data(data)
    # save_to_excel(id, data, "SimulationSimple")
    simulation_data.update_data(data, "Simple")


# ----------------------------------------------------------------------------------------------------------
def SimulationCareful_run(id, simulation_data, me_uti_data, careful, agents, neighbours, constraints):
    data = Data()  # save data here
    agents[0] = careful  # replace with special agent
    data.set_neighbours_data(neighbours)  # update data - save connections
    for agent_id in agents.keys():
        # for every agent - initiate
        a_neighbours = neighbours2agent(neighbours, agents, agent_id)
        a_constraints = constraints2agent(constraints, agent_id)
        agent = get_agent(agents, agent_id)
        agent.initiate(a_neighbours, a_constraints)
    # start running the algorithm
    i = 0
    while i < final_iteration:
        up = False
        for agent_id in agents.keys():
            agent = get_agent(agents, agent_id)
            agent.listen()
        for agent_id in agents.keys():
            agent = get_agent(agents, agent_id)
            agent.reply()
            if agent.phase == 4:
                data.update_data(agent.get_data())  # save data here
                up = True
        if up:
            i = i + 1
    data.update_best_iteration_data()
    me_uti_data.update_data(data)
    # save_to_excel(id, data, "SimulationCareful")
    simulation_data.update_data(data, "Careful")


# ----------------------------------------------------------------------------------------------------------
def SimulationGenerous_run(id, simulation_data, me_uti_data, generous, agents, neighbours, constraints):
    data = Data()  # save data here
    agents[0] = generous  # replace with special agent
    data.set_neighbours_data(neighbours)  # update data - save connections
    for agent_id in agents.keys():
        # for every agent - initiate
        a_neighbours = neighbours2agent(neighbours, agents, agent_id)
        a_constraints = constraints2agent(constraints, agent_id)
        agent = get_agent(agents, agent_id)
        agent.initiate(a_neighbours, a_constraints)
    # start running the algorithm
    i = 0
    while i < final_iteration:
        up = False
        for agent_id in agents.keys():
            agent = get_agent(agents, agent_id)
            agent.listen()
        for agent_id in agents.keys():
            agent = get_agent(agents, agent_id)
            agent.reply()
            if agent.phase == 4:
                data.update_data(agent.get_data())  # save data here
                up = True
        if up:
            i = i + 1
    data.update_best_iteration_data()
    me_uti_data.update_data(data)
    # save_to_excel(id, data, "SimulationGenerous")
    simulation_data.update_data(data, "Generous")


# ----------------------------------------------------------------------------------------------------------
def SimulationSelfish_run(id, simulation_data, me_uti_data, selfish, agents, neighbours, constraints):
    data = Data()  # save data here
    agents[0] = selfish  # replace with special agent
    data.set_neighbours_data(neighbours)  # update data - save connections
    for agent_id in agents.keys():
        # for every agent - initiate
        a_neighbours = neighbours2agent(neighbours, agents, agent_id)
        a_constraints = constraints2agent(constraints, agent_id)
        agent = get_agent(agents, agent_id)
        agent.initiate(a_neighbours, a_constraints)
    # start running the algorithm
    i = 0
    while i < final_iteration:
        up = False
        for agent_id in agents.keys():
            agent = get_agent(agents, agent_id)
            agent.listen()
        for agent_id in agents.keys():
            agent = get_agent(agents, agent_id)
            agent.reply()
            if agent.phase == 4:
                data.update_data(agent.get_data())  # save data here
                up = True
        if up:
            i = i + 1
    data.update_best_iteration_data()
    me_uti_data.update_data(data)
    # save_to_excel(id, data, "SimulationSelfish")
    simulation_data.update_data(data, "Selfish")


# ----------------------------------------------------------------------------------------------------------
def SimulationRandom_run(id, simulation_data, me_uti_data, random, agents, neighbours, constraints):
    data = Data()  # save data here
    agents[0] = random  # replace with special agent
    data.set_neighbours_data(neighbours)  # update data - save connections
    for agent_id in agents.keys():
        # for every agent - initiate
        a_neighbours = neighbours2agent(neighbours, agents, agent_id)
        a_constraints = constraints2agent(constraints, agent_id)
        agent = get_agent(agents, agent_id)
        agent.initiate(a_neighbours, a_constraints)
    # start running the algorithm
    i = 0
    while i < final_iteration:
        up = False
        for agent_id in agents.keys():
            agent = get_agent(agents, agent_id)
            agent.listen()
        for agent_id in agents.keys():
            agent = get_agent(agents, agent_id)
            agent.reply()
            if agent.phase == 4:
                data.update_data(agent.get_data())  # save data here
                up = True
        if up:
            i = i + 1
    data.update_best_iteration_data()
    me_uti_data.update_data(data)
    # save_to_excel(id, data, "SimulationRandom")
    simulation_data.update_data(data, "Random")


# ----------------------------------------------------------------------------------------------------------
def SimulationCalculated_run(id, simulation_data, me_uti_data, calculated, agents, neighbours, constraints):
    data = Data()  # save data here
    agents[0] = calculated  # replace with special agent
    data.set_neighbours_data(neighbours)  # update data - save connections
    for agent_id in agents.keys():
        # for every agent - initiate
        a_neighbours = neighbours2agent(neighbours, agents, agent_id)
        a_constraints = constraints2agent(constraints, agent_id)
        agent = get_agent(agents, agent_id)
        agent.initiate(a_neighbours, a_constraints)
    # start running the algorithm
    i = 0
    while i < final_iteration:
        up = False
        for agent_id in agents.keys():
            agent = get_agent(agents, agent_id)
            agent.listen()
        for agent_id in agents.keys():
            agent = get_agent(agents, agent_id)
            agent.reply()
            if agent.phase == 4:
                data.update_data(agent.get_data())  # save data here
                up = True
        if up:
            i = i + 1
    data.update_best_iteration_data()
    me_uti_data.update_data(data)
    # save_to_excel(id, data, "SimulationCalculated")
    simulation_data.update_data(data, "Calculated")


# _________________________________________________________________________________________________________________
def Simulation_run(id, simple_data, careful_data, generous_data, selfish_data, random_data, calculated_data):
    s = Simulation(id, 50, 10, 35)
    # --------------------------------------------same seed
    agents = s.create_agents()
    neighbours = s.create_connections()
    constraints = s.create_constraints()
    # --------------------------------------------ME agents
    simple = s.create_simple_agent()
    careful = s.create_careful_agent()
    generous = s.create_generous_agent()
    selfish = s.create_selfish_agent()
    random = s.create_random_agent()
    calculated = s.create_calculated_agent()
    # --------------------------------------------DATA
    simulation_data = SimulationData()
    # --------------------------------------------RUN
    SimulationSimple_run(id, simulation_data, simple_data, simple, copy.deepcopy(agents), copy.deepcopy(neighbours),
                         copy.deepcopy(constraints))
    SimulationCareful_run(id, simulation_data, careful_data, careful, copy.deepcopy(agents), copy.deepcopy(neighbours),
                          copy.deepcopy(constraints))
    SimulationGenerous_run(id, simulation_data, generous_data, generous, copy.deepcopy(agents), copy.deepcopy(neighbours),
                           copy.deepcopy(constraints))
    SimulationSelfish_run(id, simulation_data, selfish_data, selfish, copy.deepcopy(agents), copy.deepcopy(neighbours),
                          copy.deepcopy(constraints))
    SimulationRandom_run(id, simulation_data, random_data, random, copy.deepcopy(agents), copy.deepcopy(neighbours),
                         copy.deepcopy(constraints))
    SimulationCalculated_run(id, simulation_data, calculated_data, calculated, copy.deepcopy(agents),
                             copy.deepcopy(neighbours), copy.deepcopy(constraints))
    # --------------------------------------------Analysis
    simulation_save_to_excel(id, simulation_data)
    return simulation_data


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    sim_data = []
    simple_data = MEdata()
    careful_data = MEdata()
    generous_data = MEdata()
    selfish_data = MEdata()
    random_data = MEdata()
    calculated_data = MEdata()
    for index in range(0, 50):
        sim_data.append(Simulation_run(index, simple_data, careful_data, generous_data, selfish_data, random_data, calculated_data))
    simple_data.mean_data()
    careful_data.mean_data()
    generous_data.mean_data()
    selfish_data.mean_data()
    random_data.mean_data()
    calculated_data.mean_data()
    all_simulation_data_analysis = AllSimulationData(sim_data)
    all_simulation_data_analysis.update_data()
    analysis_save_to_excel(all_simulation_data_analysis)
    me_save_to_excel(simple_data, careful_data, generous_data, selfish_data , random_data, calculated_data)



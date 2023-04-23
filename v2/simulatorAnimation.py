import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class ParticipantAgent:
    def __init__(self, id):
        self.id = id
        self.question_rate = random.uniform(0, 1)
        self.answer_rate = random.uniform(0, 1)
        self.like_rate = random.uniform(0, 1)
        self.token_balance = 0
        self.joining_period = random.randint(1, 10)

class OrganizationAgent:
    def __init__(self):
        self.token_reward_question = 10
        self.token_reward_answer = 5
        self.token_reward_like = 1
        self.voting_period = 3
        self.saving_period = 6
        self.nft_price = 100

    def mint_nft(self, participant_agents):
        eligible_agents = [agent for agent in participant_agents if agent.token_balance >= self.nft_price]
        if eligible_agents:
            selected_agent = random.choice(eligible_agents)
            selected_agent.token_balance -= self.nft_price
            return True
        return False

def animate_simulation(simulation_history):
    fig, ax = plt.subplots()

    def update(frame_number):
        ax.clear()
        ax.bar(range(len(simulation_history[frame_number])), simulation_history[frame_number])
        ax.set_ylim(0, max(max(simulation_history)) * 1.1)
        ax.set_title(f"Month {frame_number + 1}")

    ani = FuncAnimation(fig, update, frames=len(simulation_history), repeat=False)
    plt.show()

def run_simulation(organization_agent):
    num_participants = 100
    num_months = 12
    participant_agents = [ParticipantAgent(i) for i in range(num_participants)]
    simulation_history = []

    for month in range(1, num_months + 1):
        for agent in participant_agents:
            if random.random() < agent.question_rate:
                agent.token_balance += organization_agent.token_reward_question
            if random.random() < agent.answer_rate:
                agent.token_balance += organization_agent.token_reward_answer
            if random.random() < agent.like_rate:
                agent.token_balance += organization_agent.token_reward_like

        if month % organization_agent.voting_period == 0:
            organization_agent.mint_nft(participant_agents)

        if month % organization_agent.saving_period == 0:
            for agent in participant_agents:
                agent.question_rate *= 0.9
                agent.answer_rate *= 0.9
                agent.like_rate *= 0.9
        monthly_activity = [agent.question_rate + agent.answer_rate + agent.like_rate for agent in participant_agents]
        simulation_history.append(monthly_activity)

    return simulation_history

if __name__ == "__main__":
    organization_agent = OrganizationAgent()
    simulation_history = run_simulation(organization_agent)
    animate_simulation(simulation_history)
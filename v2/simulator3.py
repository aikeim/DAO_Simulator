import random
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

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

def sweep_parameters():
    nft_prices = list(range(50, 151, 10))
    token_reward_questions = list(range(5, 16, 1))
    token_reward_answers = list(range(3, 9, 1))
    token_reward_likes = list(range(1, 4, 1))

    heatmap_data = np.zeros((len(token_reward_questions), len(nft_prices), len(token_reward_answers), len(token_reward_likes)))

    for i, token_reward_question in enumerate(token_reward_questions):
        for j, nft_price in enumerate(nft_prices):
            for k, token_reward_answer in enumerate(token_reward_answers):
                for l, token_reward_like in enumerate(token_reward_likes):
                    organization_agent = OrganizationAgent()
                    organization_agent.token_reward_question = token_reward_question
                    organization_agent.token_reward_answer = token_reward_answer
                    organization_agent.token_reward_like = token_reward_like
                    organization_agent.nft_price = nft_price

                    total_communication_activity = 0
                    num_runs = 5
                    for _ in range(num_runs):
                        total_communication_activity += run_simulation(organization_agent)
                    heatmap_data[i, j, k, l] = total_communication_activity / num_runs

    return nft_prices, token_reward_questions, token_reward_answers, token_reward_likes, heatmap_data

def plot_3d_scatter(nft_prices, token_reward_questions, token_reward_answers, token_reward_likes, heatmap_data):
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    for i, token_reward_question in enumerate(token_reward_questions):
        for j, nft_price in enumerate(nft_prices):
            for k, token_reward_answer in enumerate(token_reward_answers):
                for l, token_reward_like in enumerate(token_reward_likes):
                    total_communication_activity = heatmap_data[i, j, k, l]
                    ax.scatter(nft_price, token_reward_question, token_reward_answer, c=total_communication_activity, cmap='viridis', marker='o', s=20+total_communication_activity*2)

    ax.set_xlabel("NFT Price")
    ax.set_ylabel("Token Reward for Questions")
    ax.set_zlabel("Token Reward for Answers")
    ax.set_title("Total Communication Activity")
    plt.show()

def run_simulation(organization_agent):
    num_participants = 100
    num_months = 12
    participant_agents = [ParticipantAgent(i) for i in range(num_participants)]

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

    total_communication_activity = sum([agent.question_rate + agent.answer_rate + agent.like_rate for agent in participant_agents])
    return total_communication_activity

if __name__ == "__main__":
    nft_prices, token_reward_questions, token_reward_answers, token_reward_likes, heatmap_data = sweep_parameters()
    plot_3d_scatter(nft_prices, token_reward_questions, token_reward_answers, token_reward_likes, heatmap_data)
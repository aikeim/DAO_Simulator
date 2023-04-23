import random
import numpy as np
import pandas as pd
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class ParticipantAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.joining_period = random.randint(1, 10)
        self.question_count = max(1, 3 - 0.5 * self.joining_period) + random.uniform(-0.5, 0.5)
        self.answer_count = 1 + self.joining_period + random.uniform(-0.5, 0.5)
        self.like_count = random.randint(1, 10)
        self.token_balance = 0
        self.communication_rank = self.calculate_communication_rank()

    def calculate_communication_rank(self):
        total_count = self.question_count + self.answer_count + self.like_count
        if total_count >= 10:
            return 5
        elif total_count >= 5:
            return 3
        elif total_count >= 1:
            return 1
        else:
            return 0

    def step(self):
        self.question_count += self.model.organization_agent.token_reward_question
        self.answer_count += self.model.organization_agent.token_reward_answer
        self.like_count += self.model.organization_agent.token_reward_like
        self.token_balance += (self.question_count * self.model.organization_agent.token_reward_question +
                               self.answer_count * self.model.organization_agent.token_reward_answer +
                               self.like_count * self.model.organization_agent.token_reward_like)
        if self.token_balance >= self.model.organization_agent.nft_price:
            self.question_count += 2.0
            self.answer_count += 2.0
            self.like_count += 2.0
            self.token_balance -= self.model.organization_agent.nft_price

class OrganizationAgent(Agent):
    def __init__(self, unique_id, model, token_reward_question, token_reward_answer, token_reward_like, nft_price):
        super().__init__(unique_id, model)
        self.token_reward_question = token_reward_question
        self.token_reward_answer = token_reward_answer
        self.token_reward_like = token_reward_like
        self.nft_price = nft_price
        self.communication_rank = self.calculate_communication_rank()
        
    def step(self):
        pass

    def calculate_communication_rank(self):
        pass

class CommunicationModel(Model):
    def __init__(self, num_participants, token_reward_question, token_reward_answer, token_reward_like, nft_price):
        self.num_participants = num_participants
        self.schedule = RandomActivation(self)
        self.organization_agent = OrganizationAgent("organization", self, token_reward_question, token_reward_answer, token_reward_like, nft_price)
        self.schedule.add(self.organization_agent)

        for i in range(self.num_participants):
            participant_agent = ParticipantAgent(i, self)
            self.schedule.add(participant_agent)

        self.datacollector = DataCollector(
            agent_reporters={"CommunicationRank": "communication_rank"}
        )

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

    def calculate_communication_activation(self):
        total_communication_rank = sum([agent.communication_rank for agent in self.schedule.agents if isinstance(agent, ParticipantAgent)])
        return total_communication_rank

# Parameters
num_participants = 100
token_reward_question_values = np.linspace(0.5, 2.0, 5)
token_reward_answer_values = np.linspace(0.5, 2.0, 5)
token_reward_like_values = np.linspace(0.5, 2.0, 5)
nft_price_values = np.linspace(10, 100, 10)

# Run the simulation
simulation_results = []

for token_reward_question in token_reward_question_values:
    for token_reward_answer in token_reward_answer_values:
        for token_reward_like in token_reward_like_values:
            for nft_price in nft_price_values:
                model = CommunicationModel(num_participants, token_reward_question, token_reward_answer, token_reward_like, nft_price)
                for _ in range(36):  # 3 years (each step is one month)
                    model.step()
                communication_activation = model.calculate_communication_activation()
                simulation_results.append((token_reward_question, token_reward_answer, token_reward_like, nft_price, communication_activation))

# Store the results in a DataFrame
results_df = pd.DataFrame(simulation_results, columns=["TokenRewardQuestion", "TokenRewardAnswer", "TokenRewardLike", "NFTPrice", "CommunicationActivation"])
results_df.to_csv("simulation_results.csv", index=False)

# Find the combination that maximizes CommunicationActivation
best_result = results_df.loc[results_df["CommunicationActivation"].idxmax()]
print("Best combination:")
print(best_result)

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection="3d")

# Scatter plot
p = ax.scatter(results_df["TokenRewardQuestion"], results_df["TokenRewardAnswer"], results_df["TokenRewardLike"], c=results_df["CommunicationActivation"], cmap="viridis", alpha=0.8)

# Best result
ax.scatter(best_result["TokenRewardQuestion"], best_result["TokenRewardAnswer"], best_result["TokenRewardLike"], c="red", marker="*", s=200, label="Best Combination")

ax.set_xlabel("Token Reward (Question)")
ax.set_ylabel("Token Reward (Answer)")
ax.set_zlabel("Token Reward (Like)")

fig.colorbar(p, label="Communication Activation", pad=0.1)
plt.legend()
plt.title("3D Scatter Plot of Communication Activation")
plt.show()

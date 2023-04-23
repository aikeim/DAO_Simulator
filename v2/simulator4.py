import random
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class ParticipantAgent:
    def __init__(self, tenure):
        self.question_count = 0
        self.answer_count = 0
        self.like_count = 0
        self.token_amount = 0
        self.tenure = tenure
        self.communication_rank = 0

class OrganizationAgent:
    def __init__(self):
        self.token_reward_question = 0
        self.token_reward_answer = 0
        self.token_reward_like = 0
        self.voting_period = 3
        self.nft_price = 0
        self.communication_activation = 0

def initialize_simulation(participants, organization):
    # Set initial parameters for participant agents
    for participant in participants:
        participant.question_count = random.uniform(0.5, 2)
        participant.answer_count = random.uniform(0.5, 2)
        participant.like_count = random.uniform(0.5, 2)

    # Set initial parameters for the organization agent
    organization.token_reward_question = random.uniform(1, 5)
    organization.token_reward_answer = random.uniform(1, 5)
    organization.token_reward_like = random.uniform(1, 5)
    organization.nft_price = random.uniform(50, 200)

def run_simulation(participants, organization, months):
    for month in range(months):
        for participant in participants:
            # Update participant's token amount based on their activity
            participant.token_amount += (participant.question_count * organization.token_reward_question +
                                          participant.answer_count * organization.token_reward_answer +
                                          participant.like_count * organization.token_reward_like)
            
            # Update communication rank
            total_posts = participant.question_count + participant.answer_count + participant.like_count
            if total_posts >= 10:
                participant.communication_rank = 5
            elif total_posts >= 5:
                participant.communication_rank = 3
            elif total_posts >= 1:
                participant.communication_rank = 1
            else:
                participant.communication_rank = 0
            
            # Check if the participant can purchase NFT
            if participant.token_amount >= organization.nft_price:
                participant.question_count += 2.0
                participant.answer_count += 2.0
                participant.like_count += 2.0
                participant.token_amount -= organization.nft_price

        # Calculate the communication activation variable
        organization.communication_activation = sum([p.communication_rank for p in participants])

        # Update the simulation for the next month
        for participant in participants:
            participant.question_count -= 0.5 * participant.tenure
            participant.answer_count += 1.0 * participant.tenure
            participant.question_count = max(participant.question_count, 0)
            participant.answer_count = max(participant.answer_count, 0)
            participant.like_count = max(participant.like_count, 0)
            participant.tenure += 1/12

        if (month + 1) % organization.voting_period == 0:
            for participant in participants:
                participant.question_count += 1.0
                participant.answer_count += 1.0
                participant.like_count += 1.0

def analyze_simulation(participants, organization):
    question_counts = [p.question_count for p in participants]
    answer_counts = [p.answer_count for p in participants]
    like_counts = [p.like_count for p in participants]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(question_counts, answer_counts, like_counts)
    ax.set_xlabel('Question Count')
    ax.set_ylabel('Answer Count')
    ax.set_zlabel('Like Count')
    ax.set_title('3D Scatter Plot of Participants Activity')

    plt.show()

    communication_ranks = [p.communication_rank for p in participants]
    plt.hist(communication_ranks, bins=[0, 1, 3, 5], align='left', rwidth=0.8)
    plt.xlabel('Communication Rank')
    plt.ylabel('Number of Participants')
    plt.title('Histogram of Communication Ranks')
    plt.show()

    avg_token_amount = np.mean([p.token_amount for p in participants])
    print(f"Average token amount per participant: {avg_token_amount}")
    print(f"Organization's communication activation: {organization.communication_activation}")

def main():
    num_participants = 100
    simulation_months = 12

    participants = [ParticipantAgent(random.uniform(0, 10)) for _ in range(num_participants)]
    organization = OrganizationAgent()

    initialize_simulation(participants, organization)
    run_simulation(participants, organization, simulation_months)
    analyze_simulation(participants, organization)

if __name__ == '__main__':
    main()
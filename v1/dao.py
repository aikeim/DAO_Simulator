from variable import User, Activity, NFT, Vote, Transaction
from typing import List

class DAO:
    def __init__(self, token_incentive : int, nft_incentive : int, token_price : int, nft_price : int):
        self.users : List[User] = []
        self.activities : List[Activity] = []
        self.nfts : List[NFT] = []
        self.votes : List[Vote] = []
        self.transactions : List[Transaction] = []
        self.token_incentive = token_incentive
        self.nft_incentive = nft_incentive
        self.token_price = token_price
        self.nft_price = nft_price

    def add_user(self, user : User):
        self.users.append(user)

    def add_activity(self, activity : Activity):
        self.activities.append(activity)

    def add_nft(self, nft : NFT):
        self.nfts.append(nft)

    def add_vote(self, vote : Vote):
        self.votes.append(vote)

    def add_transaction(self, transaction : Transaction):
        self.transactions.append(transaction)

    def set_token_incentive(self, token_incentive : int):
        self.token_incentive = token_incentive

    def set_nft_incentive(self, nft_incentive : int):
        self.nft_incentive = nft_incentive

    def set_token_price(self, token_price : int):
        self.token_price = token_price

    def set_nft_price(self, nft_price : int):
        self.nft_price = nft_price

    def simulate_communication_activation(self):
        user_count = len(self.users)
        total_communication_activities = len(self.activities)

        average_activity_rate = total_communication_activities / user_count

        question_count = sum([1 for activity in self.activities if activity.activity_type == "質問"])
        answer_count = sum([1 for activity in self.activities if activity.activity_type == "回答"])
        like_count = sum([1 for activity in self.activities if activity.activity_type == "いいね"])

        diversity_of_communication_activities = {
            'questions': question_count,
            'answers': answer_count,
            'likes': like_count
        }

        # 他の評価指標を追加することもできます（例: ユーザー間の相互作用数、トピックの多様性など）

        communication_activation_score = {
            'total_communication_activities': total_communication_activities,
            'average_activity_rate': average_activity_rate,
            'diversity_of_communication_activities': diversity_of_communication_activities
        }

        return communication_activation_score
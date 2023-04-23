import random

class DAO:
    def __init__(self, token_incentive, nft_incentive, token_price, nft_price):
        self.token_incentive = token_incentive
        self.nft_incentive = nft_incentive
        self.token_price = token_price
        self.nft_price = nft_price

    def simulate_communication_activation(self):
        num_users = 100
        num_iterations = 1000
        communication_score = 0

        for _ in range(num_iterations):
            # ランダムにユーザーを選ぶ
            user = random.randint(1, num_users)

            # トークンを獲得する確率を計算
            token_probability = self.token_incentive / (self.token_incentive + self.nft_incentive)

            # NFTを獲得する確率を計算
            nft_probability = self.nft_incentive / (self.token_incentive + self.nft_incentive)

            # トークンまたはNFTを獲得するイベントをシミュレート
            reward_event = random.choices(['token', 'nft'], weights=[token_probability, nft_probability])[0]

            if reward_event == 'token':
                communication_score += user * self.token_incentive / self.token_price
            else:
                communication_score += user * self.nft_incentive / self.nft_price

        # 評価値を正規化
        communication_score /= (num_users * num_iterations)

        return communication_score
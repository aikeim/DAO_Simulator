class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.tokens = 0
        self.nfts = []
        self.activities = []

class Activity:
    def __init__(self, user_id, activity_type, timestamp, token_reward):
        self.user_id = user_id
        self.activity_type = activity_type
        self.timestamp = timestamp
        self.token_reward = token_reward

class NFT:
    def __init__(self, nft_id, creator_id, reward, price, status):
        self.nft_id = nft_id
        self.creator_id = creator_id
        self.owner_id = None
        self.mint_timestamp = None
        self.reward = reward
        self.price = price
        self.status = status

class Vote:
    def __init__(self, user_id, nft_id, tokens, timestamp):
        self.user_id = user_id
        self.nft_id = nft_id
        self.tokens = tokens
        self.timestamp = timestamp

class Transaction:
    def __init__(self, buyer_id, seller_id, nft_id, token_amount, timestamp):
        self.buyer_id = buyer_id
        self.seller_id = seller_id
        self.nft_id = nft_id
        self.token_amount = token_amount
        self.timestamp = timestamp
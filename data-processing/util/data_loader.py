import pandas as pd
import os
from util.models import Dataset

class DataLoader:
    def __init__(self, num_users, num_items, data_path):
        self.num_users = num_users
        self.num_items = num_items
        self.data_path = data_path

    # data loading
    def load(self) -> Dataset:
        ratings 
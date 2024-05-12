from abc import ABC, abstarctmethod
import sys

from util.models import Dataset, RecommendResult
from util.data_loader import DataLoader
from util.metric_caculator import MetricCalculator

# dataset 받아서 테스트 데이터 추천 결과 반환 알고리즘 구현
# BseRecommender Class 생성으로 이을 상속하는 형태로 구현

class BaseRecommender (ABC):
    @abstarctmethod
    def recommend(self, dataset: Dataset, **kwargs) -> RecommendResult:
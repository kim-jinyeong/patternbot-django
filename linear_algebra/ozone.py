import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests

class Solution:

    def __init__(self):
        url = "https://raw.githubusercontent.com/reisanar/datasets/master/ozone.data.csv"
        df = pd.read_csv(url)

        # 2. Data Preprocessing(데이터 전처리)
        # 필요한 column(Temp, Ozone)만 추출
        training_data = df[['temp', 'ozone']]

        # 결측치 제거 - dropna() 함수 이용
        self.training_data = training_data.dropna(how='any')

        # 3. Training Data Set
        self.x_data = training_data['temp'].values.reshape(-1, 1)
        self.t_data = training_data['ozone'].values.reshape(-1, 1)

        # 4. Simple Linear Regression 정의
        self.W = np.random.rand(1, 1)
        self.b = np.random.rand(1)

        # 7. 프로그램에서 필요한 변수들 정의
        self.learning_rate = 1e-5
        self.f = lambda x: self.loss_func(self.x_data, self.t_data)

    # 5. loss function 정의
    def loss_func(self, x, t):
        y = np.dot(x, self.W) + self.b
        return np.mean(np.power((t - y), 2))  # 최소제곱법

    # 6. 학습종료 후 예측값 계산 함수
    def predict(x):
        return np.dot(x, W) + b

    def solution(self):
        for step in range(90000):
            W -= self.learning_rate * self.numerical_derivative(self.f, self.W)
            b -= self.learning_rate * self.numerical_derivative(self.f, self.b)

            if step % 9000 == 0:
                print('W : {}, b : {}, loss : {}'.format(W, b, loss_func(x_data, t_data)))

        # 9. 예측
        result = predict(62)
        print(result)  # [[34.56270003]]

        # 10. 그래프로 확인
        plt.scatter(x_data, t_data)
        plt.plot(x_data, np.dot(x_data, W) + b, color='r')
        plt.show()
if __name__ == '__main__':
    Solution.solution()
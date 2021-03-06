from sklearn.datasets import load_digits
from matplotlib import rc, font_manager
import matplotlib.pylab as plt
rc('font', family=font_manager.FontProperties(fname='C:/Windows/Fonts/malgunsl.ttf').get_name())

class classnumber:
    def __init__(self):
        digits = load_digits() # 데이터 로드
        samples = [0, 10, 20, 30, 1, 11, 21, 31] # 선택된 이미지 번호
        self.d = [digits.images[samples[i]] for i in range(8)]
        self.v = [self.d[i].reshape(64, 1) for i in range(8)]# 벡터화


    def imagenumber(self):
        plt.figure(figsize=(8, 2))
        for i in range(8):
            plt.subplot(1, 8, i + 1)
            plt.imshow(self.d[i], interpolation='nearest', cmap=plt.cm.bone_r)
            plt.grid(False)
            plt.xticks([])
            plt.yticks([])
            plt.title("image {}".format(i + 1))
        plt.suptitle("숫자 0과 1 이미지")
        plt.tight_layout()
        plt.show()

    def imagevector(self):
        plt.figure(figsize=(8, 3))
        for i in range(8):
            plt.subplot(1, 8, i + 1)
            plt.imshow(self.v[i], aspect=0.4,interpolation='nearest', cmap=plt.cm.bone_r)
            plt.grid(False)
            plt.xticks([])
            plt.yticks([])
            plt.title("벡터 {}".format(i + 1))
        plt.suptitle("벡터화된 이미지", y=1.05)
        plt.tight_layout(w_pad=7)
        plt.show()

if __name__ == '__main__':
    classnumber().imagenumber()
    classnumber().imagevector()
from context.domains import Reader, File


class Solution(Reader, File):
    def __init__(self):
        self.context = './data'
        self.crime_rate_columns = ['살인검거율', '강도검거율', '강간검거율', '절도검거율', '폭력검거율']
        self.crime_columns = ['살인', '강도', '강간', '절도', '폭력']
    def save_police_pos(self):
        self.fname = 'crime_in_seoul'
        self.printer(self.csv(File))

    def save_cctv_pos(self):
        self.fname = 'cctv_in_seoul'
        self.printer(self.csv(File))

    def save_police_norm(self):
        self.fname = 'geo_simple'
        self.printer(self.json(File))

    def folium_test(self):
        pass

    def draw_crime_map(self):
        pass


if __name__ == '__main__':
    Solution().save_police_pos()
    Solution().save_cctv_pos()
    Solution().save_police_norm()

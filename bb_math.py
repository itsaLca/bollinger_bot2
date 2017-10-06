import numpy as np
from sortedcontainers import SortedDict
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as md



class bb_math:

    def __init__(self):
        self.input_dict = {}
        self.running_avg = {}
        self.std_value = None
        self.upper_line = {}
        self.lower_line = {}

    def moving_average(self, x, N):
        if (len(x)<N):
            return x[0]
        else:
            return np.convolve(x, np.ones((N,)) / N, mode='valid')[-1:][0]


    def moving_average_dict(self, sorted_dict):
        tmp_lst = []
        return_sorted_dict = {}
        for item in sorted_dict.keys():
            time_st = item
            price = sorted_dict[item]
            tmp_lst.append(price)
            tmp_var = self.moving_average(tmp_lst, 3)
            return_sorted_dict[item] = tmp_var
        return_sorted_dict = SortedDict(return_sorted_dict)
        return return_sorted_dict

    def moving_average_FOUR(self, sorted_dict, num_avg):
        for i in range(num_avg):
            sorted_dict = self.moving_average_dict(sorted_dict)
        return sorted_dict

    def bb_std(self, sorted_dict):
        self.std_value = None
        self.std_value = np.std(sorted_dict.values())
        self.std_value = float(self.std_value)
        return self.std_value

    def bb_upper_line(self):
        self.upper_line = {}
        upper_line = float(self.running_avg.values()[-1:][0]) + (2 * self.std_value)
        time_st = self.running_avg.keys()[-1:][0]
        self.upper_line[time_st] = upper_line
        self.upper_line = SortedDict(self.upper_line)
        return self.upper_line

    def bb_lower_line(self):
        self.lower_line = {}
        lower_line = float(self.running_avg.values()[-1:][0]) - (2 * self.std_value)
        time_st = self.running_avg.keys()[-1:][0]
        self.lower_line[time_st] = lower_line
        self.lower_line = SortedDict(self.lower_line)
        return self.lower_line

    def bb_compare_to_buy(self, curPrice, lower_line, upper_line, percent):
        if ((curPrice < (lower_line + ((upper_line - lower_line) * percent * 0.01))) and (curPrice > lower_line)) or curPrice > upper_line :
            return True
        else:
            return False

    def bb_compare_to_sell(self, curPrice, lower_line, upper_line, percent):
        if ((curPrice > (upper_line - ((upper_line - lower_line) * percent * 0.01))) and (curPrice < upper_line)) or curPrice < lower_line:
            return True
        else:
            return False

    def bb_plot(self, sort_Dict_price, sort_Dict_avg, sort_Dict_upp, sort_Dict_low, cryptocurrency):
        plt.grid()
        my_labels = {"sort_Dict_price": "price_usd", "sort_Dict_avg": "mov_avg", "sort_Dict_upp": "upp_bbl", "sort_Dict_low": "low_bbl"}
        dates_price = [dt.datetime.fromtimestamp(ts) for ts in sort_Dict_price.keys()]
        dates_last_point = [dt.datetime.fromtimestamp(ts) for ts in sort_Dict_upp.keys()]

        plt.subplots_adjust(bottom=0.2)
        plt.xticks(rotation=25)
        ax = plt.gca()
        xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
        ax.xaxis.set_major_formatter(xfmt)

        scat1 = plt.plot(dates_price, sort_Dict_price.values(), color='red', marker='o', linestyle='--', label=my_labels["sort_Dict_price"])
        scat2 = plt.plot(dates_price, sort_Dict_avg.values(), color='blue', marker='o', linestyle='--', label=my_labels["sort_Dict_avg"])
        scat3 = plt.plot(dates_last_point, sort_Dict_upp.values(), color='green', marker='o', linestyle='--', label=my_labels["sort_Dict_upp"])
        scat4 = plt.plot(dates_last_point, sort_Dict_low.values(), color='green', marker='o', linestyle='--', label=my_labels["sort_Dict_low"])

        plt.legend(loc='best')
        #plt.show()

        if cryptocurrency is not 'BTC':
            filename = cryptocurrency + '_BTC.png'
        else:
            filename = 'BTC_USD.png'

        #file = open(filename, "w")
        with open(filename, 'w') as f:
            f.close()

        filename_without_extension = filename.split('.')[0]

        plt.savefig(filename_without_extension)

        #plt.savefig("fig_1")
        plt.clf()
        #plt.cla()

def main():
    pass

    running_avg_FIRST = []
    running_avg_SECOND = []
    running_avg_THIRD = []

    math = bb_math()
    math.running_avg = math.moving_average_FOUR(math.input_dict, 4)
    math.std_dict = math.bb_std(math.input_dict)
    math.upper_line = math.bb_upper_line()
    math.lower_line = math.bb_lower_line()

    if (math.bb_compare_to_buy(math.input_dict.values()[-1:][0],math.lower_line.values()[-1:][0], math.upper_line.values()[-1:][0] ), 5):
        print("BUY")

    if (math.bb_compare_to_sell(math.input_dict.values()[-1:][0], math.lower_line.values()[-1:][0], math.upper_line.values()[-1:][0]), 5):
        print("SELL")

    #math.bb_plot(math.input_dict, math.running_avg, math.upper_line, math.lower_line, cryptocurrency)


if __name__ == "__main__":
    main()
from newsworthycharts import SerialChart
import numpy as np

class TemperatueChart(SerialChart):
    def _add_data(self):
        self.color_fn = "positive_negative"
        if len(self.data) != 1:
            raise ValueError("TemperatueChart takes one and only one data series.")

        dates = [x[0] for x in self.data[0]]
        values = [x[1] for x in self.data[0]]
        s = np.array(values, dtype=np.float)
        mean = np.nanmean(s)
        vs_mean = s - mean
        self.data[0] = list(zip(dates, vs_mean.tolist()))
        self._ymin = np.nanmin(vs_mean)
        self.data.max_val = np.nanmax(vs_mean)
        

        super(TemperatueChart, self)._add_data()

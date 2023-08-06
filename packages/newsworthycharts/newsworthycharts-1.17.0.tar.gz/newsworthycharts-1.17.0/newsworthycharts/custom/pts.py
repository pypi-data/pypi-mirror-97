"""Custom charts for bredbandsutredningen.
"""

from newsworthycharts import CategoricalChart

class BroadbandTargetChart(CategoricalChart):
    def _add_data(self):
        super(BroadbandTargetChart, self)._add_data()

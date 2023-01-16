'''Custom Summary Stats'''

import pandas

Telco = pandas.read_excel('/Users/carstenjuliansavage/PycharmProjects/Random_Project/Telco_customer_churn.xlsx')
$
def percentile(n):
    def percentile_(x):
        return x.quantile(n)
    percentile_.__name__ = 'Percentile_{:2.0f}'.format(n*100)
    return percentile_

summary_stats = (Telco
    .groupby(['City'])
    .agg({'min',
          'max',
          'mean',
          'median',
          'var',
          percentile(0.47),
          percentile(0.99)})
    .stack(0)
    .rename(columns={'min':"Min",'max':"Max",'mean':"Mean",'median':"Median",'var':"Variance"})
    #.iloc[:, [5, 4, 3, 2, 0, 1, 6]]- # To reorder columns, if necessary
)

summary_stats.to_excel("/Users/carstenjuliansavage/Desktop/R Working Directory/Python/summary_stats.xlsx")
import pandas as pd
import numpy as np

# df = pd.DataFrame(data = np.array([[0.81, 0.96, 0.94, 0.99],
#                               [0.64, 0.36, 0.28, 0.97],
#                               [0.60, 0.47, 0.25, 0.90],
#                               [0.62, 0.96, 0.96, 0.06]]), 
#              columns = ['prec', 'recall', 'prec', 'recall'], 
#              index = ['Normal', 'Cap', 'UPPER', 'lower'])


# df = pd.DataFrame(data = [["apple, the fruit", "Apple, the company"], 
#                           ["us, the pronoun", "US, the country"], 
#                           ["Windows, the operating system", "windows, opening in the wall"]],
#                   columns = ['Original', 'Transformed'], 
#                   index = ['Cap', 'UPPER', 'lower'])

df = pd.DataFrame(data = [[0.93, 0.94, 0.97, 0.92, 0.97, 0.95],
                          [0.82, 0.88, 0.24, 0.88, 0.92, 0.87],
                          [0.79, 0.86, 0.89, 0.75, 0.97, 0.82],
                          [1.00, 0.13, 1.00, 0.03, 1.00, 0.01]],
                  columns = ['Prec', 'Rec', 'Prec', 'Rec', 'Prec', 'Rec'], 
                  index = ['Normal', 'Cap', 'UPPER', 'lower'])
print df.to_latex()




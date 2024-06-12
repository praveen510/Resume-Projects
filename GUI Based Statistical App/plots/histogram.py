import matplotlib.pyplot as plt
import seaborn as sns

def plot_histogram(data, column):
    plt.figure(figsize=(10, 6))
    sns.histplot(data[column])
    plt.xlabel(column)
    plt.ylabel('Frequency')
    plt.title(f'Histogram of {column}')
    plt.show()

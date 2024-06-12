import matplotlib.pyplot as plt

def plot_scatter(data, x_column, y_column):
    plt.figure(figsize=(10, 6))
    plt.scatter(data[x_column], data[y_column])
    plt.title(f'Scatter Plot of {x_column} vs {y_column}')
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.show()

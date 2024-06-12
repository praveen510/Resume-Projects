import matplotlib.pyplot as plt

def plot_box(data, column):
    if column in data.columns and data[column].dtype.kind in 'biufc':
        plt.figure(figsize=(10, 6))
        data[[column]].boxplot()
        plt.title(f'Box Plot of {column}')
        plt.ylabel(column)
        plt.show()
    else:
        print(f"Cannot create box plot for non-numeric column: {column}")

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QListWidget, QTableWidget, QTableWidgetItem, QInputDialog
import pandas as pd
from ui.main_window import Ui_MainWindow
from analysis.descriptive import descriptive_statistics
from analysis.crosstab import create_crosstab
from plots.histogram import plot_histogram
from plots.barplot import plot_bar
from plots.scatterplot import plot_scatter
from plots.boxplot import plot_box

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.data = None
        self.loadButton.clicked.connect(self.load_data)
        self.saveButton.clicked.connect(self.save_data)
        self.describeButton.clicked.connect(self.show_descriptive_stats)
        self.histButton.clicked.connect(self.plot_histogram)
        self.barButton.clicked.connect(self.plot_bar)
        self.resetButton.clicked.connect(self.reset_application)
        self.scatterButton.clicked.connect(self.plot_scatter)
        self.boxButton.clicked.connect(self.plot_box)
        self.crossTabButton.clicked.connect(self.show_crosstab)
        self.columnListWidget.setSelectionMode(QListWidget.MultiSelection)
        self.columnListWidget.setDragEnabled(True)
        self.plotDropArea.setAcceptDrops(True)
        self.plotDropArea.dragEnterEvent = self.dragEnterEvent
        self.plotDropArea.dropEvent = self.dropEvent
    
    def reset_application(self):
        # Reset the state of the application
        self.data = None
        self.columnListWidget.clear()
        self.crosstabTable.clearContents()
        self.crosstabTable.setRowCount(0)  # Clear all rows
        self.crosstabTable.setColumnCount(0)  # Clear all columns
        self.crosstabTable.setHorizontalHeaderLabels([])  # Clear horizontal header labels
        self.statusbar.clearMessage()
        self.columnListWidget.clearSelection()


    def load_data(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'CSV files (*.csv);;Excel files (*.xlsx *.xls)')
        if file_path:
            try:
                # Get all sheet names from the Excel file
                sheet_names = pd.ExcelFile(file_path).sheet_names
    
                # Prompt the user to select a sheet from the list
                selected_sheet, ok = QInputDialog.getItem(self, "Select Sheet", "Select a sheet:", sheet_names, 0, False)
                if ok:
                    if file_path.endswith('.csv'):
                        self.data = pd.read_csv(file_path)
                    elif file_path.endswith(('.xlsx', '.xls')):
                        self.data = pd.read_excel(file_path, sheet_name=selected_sheet)
                    self.statusbar.showMessage(f"Loaded data from {file_path}, Sheet: {selected_sheet}")
                    self.update_column_list()
            except Exception as e:
                QMessageBox.warning(self, "Error", str(e))



    def save_data(self):
        if self.data is not None:
            file_path, _ = QFileDialog.getSaveFileName(self, 'Save File', '', 'CSV files (*.csv);;Excel files (*.xlsx *.xls)')
            if file_path:
                if file_path.endswith('.csv'):
                    self.data.to_csv(file_path, index=False)
                elif file_path.endswith(('.xlsx', '.xls')):
                    self.data.to_excel(file_path, index=False)
                self.statusbar.showMessage(f"Saved data to {file_path}")
        else:
            QMessageBox.warning(self, "Warning", "No data to save!")

    def show_descriptive_stats(self):
        if self.data is not None:
            stats = descriptive_statistics(self.data)
            QMessageBox.information(self, "Descriptive Statistics", stats.to_string())
        else:
            QMessageBox.warning(self, "Warning", "No data loaded!")

    def plot_histogram(self):
        selected_items = self.columnListWidget.selectedItems()
        if self.data is not None and selected_items:
            column_name = selected_items[0].text()
            plot_histogram(self.data, column_name)
        else:
            QMessageBox.warning(self, "Warning", "No data loaded or no column selected!")

    def plot_bar(self):
        selected_items = self.columnListWidget.selectedItems()
        if self.data is not None and selected_items:
            column_name = selected_items[0].text()
            plot_bar(self.data, column_name)
        else:
            QMessageBox.warning(self, "Warning", "No data loaded or no column selected!")

    def plot_scatter(self):
        selected_items = self.columnListWidget.selectedItems()
        if self.data is not None and len(selected_items) == 2:
            x_column = selected_items[0].text()
            y_column = selected_items[1].text()
            plot_scatter(self.data, x_column, y_column)
        else:
            QMessageBox.warning(self, "Warning", "Select exactly 2 columns for scatter plot!")

    def plot_box(self):
        selected_items = self.columnListWidget.selectedItems()
        if self.data is not None and selected_items:
            column_name = selected_items[0].text()
            plot_box(self.data, column_name)
        else:
            QMessageBox.warning(self, "Warning", "No data loaded or no column selected!")

    def display_crosstab(self, crosstab):
        self.crosstabTable.setRowCount(crosstab.shape[0])
        self.crosstabTable.setColumnCount(crosstab.shape[1])
        self.crosstabTable.setHorizontalHeaderLabels(crosstab.columns.astype(str))
        self.crosstabTable.setVerticalHeaderLabels(crosstab.index.astype(str))
        for i in range(crosstab.shape[0]):
            for j in range(crosstab.shape[1]):
                self.crosstabTable.setItem(i, j, QTableWidgetItem(str(crosstab.iat[i, j])))

    def update_column_list(self):
        self.columnListWidget.clear()
        if self.data is not None:
            self.columnListWidget.addItems(self.data.columns)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('application/x-qabstractitemmodeldatalist'):
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasFormat('application/x-qabstractitemmodeldatalist'):
            selected_items = self.columnListWidget.selectedItems()
            if self.data is not None and len(selected_items) == 2:
                index_col = selected_items[0].text()
                columns_col = selected_items[1].text()
                value_col, ok = QInputDialog.getText(self, "Input", "Enter value column name:")
                if ok and value_col in self.data.columns:
                    crosstab = create_crosstab(self.data, index_col, columns_col, value_col)
                    self.display_crosstab(crosstab)
                else:
                    QMessageBox.warning(self, "Warning", "Invalid value column name!")
                event.accept()
            else:
                event.ignore()

    def show_crosstab(self):
        selected_items = self.columnListWidget.selectedItems()
        if self.data is not None and len(selected_items) == 2:
            index_col = selected_items[0].text()
            columns_col = selected_items[1].text()
            value_col, ok = QInputDialog.getText(self, "Input", "Enter value column name:")
            if ok and value_col in self.data.columns:
                agg_func, ok = QInputDialog.getItem(self, "Select Aggregation Function", "Choose an aggregation function:", 
                                                     ["count", "mean", "max", "std", "round_mean", "round_max", "round_std", "corr"], 0, False)
                if ok:
                    crosstab = create_crosstab(self.data, index_col, columns_col, value_col, agg_func)
                    self.display_crosstab(crosstab)
            else:
                QMessageBox.warning(self, "Warning", "Invalid value column name!")
        else:
            QMessageBox.warning(self, "Warning", "Please select exactly 2 columns for cross-tabulation!")
    

app = QApplication([])
window = MainWindow()
window.show()
app.exec_()

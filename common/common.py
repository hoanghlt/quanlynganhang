def autosizeColumns(tableWidget):
        total_width = tableWidget.verticalHeader().width()  # Bao gồm cả cột index
        total_width += tableWidget.horizontalHeader().length()  # Bao gồm cả hàng index

        for col in range(tableWidget.columnCount()):
            total_width += tableWidget.columnWidth(col)

        viewport_width = tableWidget.viewport().width()
        if total_width > viewport_width:
            ratio = viewport_width / total_width
            for col in range(tableWidget.columnCount()):
                tableWidget.setColumnWidth(
                    col, int(tableWidget.columnWidth(col) * ratio))
        else:
            for col in range(tableWidget.columnCount()):
                tableWidget.setColumnWidth(
                    col, tableWidget.horizontalHeader().defaultSectionSize())
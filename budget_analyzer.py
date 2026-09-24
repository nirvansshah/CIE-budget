import sys
try:
    from PyQt5.QtWidgets import (
        QApplication, QWidget, QLabel, QLineEdit,
        QPushButton, QTextEdit, QVBoxLayout, QFormLayout,
        QMessageBox, QTableWidget, QTableWidgetItem
    )
    import matplotlib.pyplot as plt
except ImportError:
    error_message = "Please install required Libraries:\n\npip install PyQt5 matplotlib"
    print(error_message)
    sys.exit(1)  # Exit the program gracefully

# function to add month data into table
def addMonth():
    try:
        # taking inputs from boxes
        inc = incBox.text().strip()
        fix = fixBox.text().strip()
        var = varBox.text().strip()
        save = saveBox.text().strip()
        unexp = unexpBox.text().strip()
        budg = budgBox.text().strip()

        if inc == "" or fix == "" or var == "" or save == "" or unexp == "" or budg == "":
            raise ValueError("empty field")

        # convert to numbers
        inc = float(inc)
        fix = float(fix)
        var = float(var)
        save = float(save)
        unexp = float(unexp)
        budg = float(budg)

        # add to table
        row = monthTable.rowCount()
        monthTable.insertRow(row)
        monthTable.setItem(row, 0, QTableWidgetItem(str(inc)))
        monthTable.setItem(row, 1, QTableWidgetItem(str(fix)))
        monthTable.setItem(row, 2, QTableWidgetItem(str(var)))
        monthTable.setItem(row, 3, QTableWidgetItem(str(save)))
        monthTable.setItem(row, 4, QTableWidgetItem(str(unexp)))
        monthTable.setItem(row, 5, QTableWidgetItem(str(budg)))

        # clear input boxes
        incBox.clear()
        fixBox.clear()
        varBox.clear()
        saveBox.clear()
        unexpBox.clear()
        budgBox.clear()

    except:
        QMessageBox.warning(win, "Error", "Please put valid numbers in all fields")

# function to check and make report
def analyze():
    rows = monthTable.rowCount()
    if rows == 0:
        QMessageBox.warning(win, "Error", "No months added")
        return

    incomes = []
    spents = []
    budgs = []
    reportLines = []

    for r in range(rows):
        try:
            inc = float(monthTable.item(r, 0).text())
            fix = float(monthTable.item(r, 1).text())
            var = float(monthTable.item(r, 2).text())
            save = float(monthTable.item(r, 3).text())
            unexp = float(monthTable.item(r, 4).text())
            budg = float(monthTable.item(r, 5).text())

            totalSpent = fix + var + unexp
            left = inc - totalSpent
            savingsDone = left >= save

            if totalSpent > inc:
                stat = "Overspending"
                health = "Critical"
            elif totalSpent > budg:
                stat = "Over Budget"
                health = "Caution"
            else:
                stat = "Within Budget"
                if savingsDone:
                    health = "Stable"
                else:
                    health = "Caution"

            tips = []
            if not savingsDone:
                tips.append("Try to save more money.")
            if unexp > 0.2 * inc:
                tips.append("Unexpected costs too high.")
            if var > 0.4 * inc:
                tips.append("Variable expenses are high.")
            if len(tips) == 0:
                tips.append("Good job, keep going!")

            incomes.append(inc)
            spents.append(totalSpent)
            budgs.append(budg)

            rep = f"Month {r+1}:\nStatus: {stat}\nHealth: {health}\nIncome: ₹{inc}, Spent: ₹{totalSpent}, Budget: ₹{budg}\nTips:\n"
            for t in tips:
                rep += "- " + t + "\n"
            reportLines.append(rep)

        except:
            QMessageBox.warning(win, "Error", f"Problem in month {r+1}")
            return

    # show text report
    outBox.setPlainText("\n".join(reportLines))

    # draw graph
    months = list(range(1, len(incomes) + 1))
    plt.figure(figsize=(9, 5))
    plt.plot(months, incomes, marker='o', label="Income", color="green")
    plt.plot(months, spents, marker='o', label="Spent", color="red")
    plt.plot(months, budgs, marker='o', label="Budget", color="blue", linestyle="--")
    plt.xticks(months)
    plt.xlabel("Month")
    plt.ylabel("₹ Amount")
    plt.title("Budget Chart")
    plt.legend()
    plt.grid(True)
    plt.show()

# main app
app = QApplication(sys.argv)
win = QWidget()
win.setWindowTitle("Budget Checker")
win.setGeometry(300, 200, 700, 650)

# form
form = QFormLayout()
incBox = QLineEdit()
fixBox = QLineEdit()
varBox = QLineEdit()
saveBox = QLineEdit()
unexpBox = QLineEdit()
budgBox = QLineEdit()

form.addRow("Monthly Income:", incBox)
form.addRow("Fixed Expenses:", fixBox)
form.addRow("Variable Expenses:", varBox)
form.addRow("Savings Goal:", saveBox)
form.addRow("Unexpected Expenses:", unexpBox)
form.addRow("Budget Limit:", budgBox)

# buttons
addBtn = QPushButton("Add Month")
addBtn.clicked.connect(addMonth)

analyzeBtn = QPushButton("Analyze")
analyzeBtn.clicked.connect(analyze)

# table
monthTable = QTableWidget()
monthTable.setColumnCount(6)
monthTable.setHorizontalHeaderLabels([
    "Income", "Fixed", "Variable", "Savings Goal", "Unexpected", "Budget"
])

# output box
outBox = QTextEdit()
outBox.setReadOnly(True)

# layout
layout = QVBoxLayout()
layout.addLayout(form)
layout.addWidget(addBtn)
layout.addWidget(monthTable)
layout.addWidget(analyzeBtn)
layout.addWidget(QLabel("Results:"))
layout.addWidget(outBox)

win.setLayout(layout)
win.show()
sys.exit(app.exec_())

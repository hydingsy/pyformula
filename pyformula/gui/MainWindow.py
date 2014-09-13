from PySide import QtCore, QtGui
from ..formulae import guided


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self._init_ui()
        self.fill_function_combo()
        self.refresh_function_switch()
        self.refresh_input_widget()

        self.calc()

        self.function_combo.currentIndexChanged.connect(
            self.refresh_function_switch)
        self.function_combo.currentIndexChanged.connect(
            self.refresh_input_widget)

    def _init_ui(self):
        self.central_widget = QtGui.QWidget(self)
        self.setCentralWidget(self.central_widget)

        function_layout = QtGui.QHBoxLayout()
        self.function_lbl = QtGui.QLabel(self.tr("Functie:"))
        self.function_combo = QtGui.QComboBox()
        function_layout.addWidget(self.function_lbl)
        function_layout.addWidget(self.function_combo)

        desc_layout = QtGui.QHBoxLayout()
        self.desc_lbl = QtGui.QLabel(self.tr("foo"))
        desc_layout.addWidget(self.desc_lbl)

        # To be filled depending on selected function.
        input_layout = QtGui.QVBoxLayout()
        self.input_widget = QtGui.QStackedWidget()
        input_layout.addWidget(self.input_widget)

        # create list: [[label, spin], [label, spin]]
        # self.input_layout.addWidget(lst[0][0])
        # self.input_layout.addWidget(lst[0][1])

        answer_layout = QtGui.QVBoxLayout()
        self.answer_lbl = QtGui.QLabel(self.tr("N/A"))
        answer_layout.addWidget(self.answer_lbl)

        layout = QtGui.QVBoxLayout()
        layout.addLayout(function_layout)
        layout.addLayout(desc_layout)
        layout.addLayout(input_layout)
        layout.addLayout(answer_layout)
        self.central_widget.setLayout(layout)

    def fill_function_combo(self):
        # We'll have to manually add all functions here.  It's a shit solution,
        # but it's the best we've got.
        self.function_combo.addItem(guided.abc.name, guided.abc)
        self.function_combo.addItem("hello", guided.Function("a", "b", ["c"]))

    def refresh_function_switch(self):
        index = self.function_combo.currentIndex()
        function = self.function_combo.itemData(index)

        self.desc_lbl.setText(function.expr)

    def refresh_input_widget(self):
        index = self.function_combo.currentIndex()
        function = self.function_combo.itemData(index)

        self.input_widget.addWidget(InputWidget(function))
        self.input_widget.setCurrentIndex(self.input_widget.count()-1)

    def calc(self):
        args = {}

        for key, spin in self.input_widget.currentWidget().spins.items():
            args[key] = spin.value()

        #print(guided.abc(args))

class InputWidget(QtGui.QWidget):
    def __init__(self, function):
        super(InputWidget, self).__init__()

        self.spins = {}

        layout = QtGui.QVBoxLayout()

        for arg in function.args:
            hor_layout = QtGui.QHBoxLayout()
            label = QtGui.QLabel("{}:".format(arg))
            dspinbox = QtGui.QDoubleSpinBox()
            hor_layout.addWidget(label)
            hor_layout.addWidget(dspinbox)

            layout.addLayout(hor_layout)

            self.spins[arg] = dspinbox

        #layout = QtGui.QVBoxLayout()
        #layout.addWidget(QtGui.QLabel("Hello"))

        self.setLayout(layout)

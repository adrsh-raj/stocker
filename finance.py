import sys
import logging
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QFormLayout, QLabel, QLineEdit, QPushButton, QGroupBox, 
                            QTabWidget, QTextEdit, QStatusBar, QMessageBox, QFileDialog,
                            QDoubleSpinBox, QSpinBox, QComboBox, QFrame, QScrollArea)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont, QIcon
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('financial_calculator.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class FinancialCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Professional Financial Calculator")
        self.setGeometry(100, 100, 1000, 700)
        
        # Initialize variables
        self.list_append = []
        self.list_append_b = []
        self.sixth_term = 0
        self.new_list = []
        self.sumofvalues = 0
        self.Terminal_Value = 0
        self.formula = 0
        self.netcash = 0
        self.totalShare = 0
        
        self.init_ui()
        self.create_menu()
        self.create_status_bar()
        
    def init_ui(self):
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        
        # Create tabs
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        # Create calculator tab
        self.create_calculator_tab()
        
        # Create visualization tab
        self.create_visualization_tab()
        
        # Create log viewer tab
        self.create_log_tab()
        
        # Apply styles
        self.apply_styles()
        
    def create_calculator_tab(self):
        """Create the main calculator tab with all financial calculation widgets"""
        calculator_tab = QWidget()
        calculator_layout = QVBoxLayout(calculator_tab)
        
        # Create scroll area for the calculator tab
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(calculator_tab)
        
        # Add header
        header = QLabel("Financial Valuation Calculator")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_font = QFont()
        header_font.setPointSize(16)
        header_font.setBold(True)
        header.setFont(header_font)
        calculator_layout.addWidget(header)
        
        # Add date label
        date_label = QLabel(f"Date: {QDate.currentDate().toString('dddd, MMMM d, yyyy')}")
        date_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        calculator_layout.addWidget(date_label)
        
        # Create form groups with proper spacing
        self.create_future_value_group(calculator_layout)
        calculator_layout.addSpacing(15)
        
        self.create_npv_group(calculator_layout)
        calculator_layout.addSpacing(15)
        
        self.create_terminal_value_group(calculator_layout)
        calculator_layout.addSpacing(15)
        
        self.create_fair_value_group(calculator_layout)
        calculator_layout.addSpacing(15)
        
        # Add buttons
        self.create_button_group(calculator_layout)
        
        # Add stretch to push content up
        calculator_layout.addStretch()
        
        # Add the scroll area to a container widget
        container = QWidget()
        container.setLayout(QVBoxLayout())
        container.layout().addWidget(scroll)
        self.tabs.addTab(container, "Calculator")
    
    def create_future_value_group(self, parent_layout):
        """Create the Future Value calculation group"""
        group = QGroupBox("Future Cash Flow Calculations")
        group_layout = QVBoxLayout()
        group_layout.setSpacing(10)
        
        # First future value calculation
        fv1_layout = QHBoxLayout()
        fv1_layout.addWidget(QLabel("Initial Amount (CF):"))
        self.amount_future = QDoubleSpinBox()
        self.amount_future.setRange(0, 999999999)
        self.amount_future.setPrefix("Rs. ")
        self.amount_future.setValue(80.00)
        fv1_layout.addWidget(self.amount_future)
        
        fv1_layout.addWidget(QLabel("Growth Rate (%):"))
        self.operation_future = QDoubleSpinBox()
        self.operation_future.setRange(-100, 1000)
        self.operation_future.setSuffix(" %")
        self.operation_future.setValue(15.00)
        fv1_layout.addWidget(self.operation_future)
        
        fv1_layout.addWidget(QLabel("Years:"))
        self.future_year_entry = QSpinBox()
        self.future_year_entry.setRange(1, 100)
        self.future_year_entry.setValue(5)
        fv1_layout.addWidget(self.future_year_entry)
        
        self.future_button = QPushButton("Calculate FV")
        self.future_button.clicked.connect(self.FvCalculator)
        fv1_layout.addWidget(self.future_button)
        
        group_layout.addLayout(fv1_layout)
        
        # Second future value calculation
        fv2_layout = QHBoxLayout()
        fv2_layout.addWidget(QLabel("Secondary Amount (CF2):"))
        self.amount_future_b = QDoubleSpinBox()
        self.amount_future_b.setRange(0, 999999999)
        self.amount_future_b.setPrefix("Rs. ")
        self.amount_future_b.setValue(117.00)
        fv2_layout.addWidget(self.amount_future_b)
        
        fv2_layout.addWidget(QLabel("Growth Rate (%):"))
        self.operation_future_b = QDoubleSpinBox()
        self.operation_future_b.setRange(-100, 1000)
        self.operation_future_b.setSuffix(" %")
        self.operation_future_b.setValue(8.00)
        fv2_layout.addWidget(self.operation_future_b)
        
        fv2_layout.addWidget(QLabel("Years:"))
        self.future_year_entry_b = QSpinBox()
        self.future_year_entry_b.setRange(1, 100)
        self.future_year_entry_b.setValue(5)
        fv2_layout.addWidget(self.future_year_entry_b)
        
        self.future_button_b = QPushButton("Calculate FV2")
        self.future_button_b.clicked.connect(self.FvCalculator_b)
        fv2_layout.addWidget(self.future_button_b)
        
        group_layout.addLayout(fv2_layout)
        
        # Results display with scrollable area
        result_scroll = QScrollArea()
        result_scroll.setWidgetResizable(True)
        result_container = QWidget()
        result_container_layout = QVBoxLayout(result_container)
        
        self.fv_result_label = QLabel()
        self.fv_result_label.setWordWrap(True)
        self.fv_result_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        result_container_layout.addWidget(self.fv_result_label)
        
        result_scroll.setWidget(result_container)
        result_scroll.setMinimumHeight(120)
        group_layout.addWidget(result_scroll)
        
        group.setLayout(group_layout)
        parent_layout.addWidget(group)
    
    def create_npv_group(self, parent_layout):
        """Create the NPV calculation group"""
        group = QGroupBox("Net Present Value Calculation")
        group_layout = QVBoxLayout()
        group_layout.setSpacing(10)
        
        # Discount rate selection
        rate_layout = QHBoxLayout()
        rate_layout.addWidget(QLabel("Discount Rate:"))
        self.discount_rate = QDoubleSpinBox()
        self.discount_rate.setRange(0, 100)
        self.discount_rate.setValue(9.0)
        self.discount_rate.setSuffix(" %")
        rate_layout.addWidget(self.discount_rate)
        
        self.npv_button = QPushButton("Calculate NPV")
        self.npv_button.clicked.connect(self.Nv)
        self.npv_button.setEnabled(False)
        rate_layout.addWidget(self.npv_button)
        
        group_layout.addLayout(rate_layout)
        
        # Results display with scrollable area
        result_scroll = QScrollArea()
        result_scroll.setWidgetResizable(True)
        result_container = QWidget()
        result_container_layout = QVBoxLayout(result_container)
        
        self.npv_result_label = QLabel()
        self.npv_result_label.setWordWrap(True)
        self.npv_result_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        result_container_layout.addWidget(self.npv_result_label)
        
        result_scroll.setWidget(result_container)
        result_scroll.setMinimumHeight(120)
        group_layout.addWidget(result_scroll)
        
        group.setLayout(group_layout)
        parent_layout.addWidget(group)
    
    def create_terminal_value_group(self, parent_layout):
        """Create the Terminal Value calculation group"""
        group = QGroupBox("Terminal Value Calculation")
        group_layout = QVBoxLayout()
        group_layout.setSpacing(10)
        
        # Terminal growth rate
        growth_layout = QHBoxLayout()
        growth_layout.addWidget(QLabel("Terminal Growth Rate:"))
        self.terminal_growth = QDoubleSpinBox()
        self.terminal_growth.setRange(-10, 10)
        self.terminal_growth.setValue(3.5)
        self.terminal_growth.setSuffix(" %")
        growth_layout.addWidget(self.terminal_growth)
        
        self.terminal_button = QPushButton("Calculate Terminal Value")
        self.terminal_button.clicked.connect(self.TerminalValue)
        self.terminal_button.setEnabled(False)
        growth_layout.addWidget(self.terminal_button)
        
        group_layout.addLayout(growth_layout)
        
        # Present value calculation
        pv_layout = QHBoxLayout()
        pv_layout.addWidget(QLabel("Present Value of Terminal Value:"))
        self.pv_button = QPushButton("Calculate PV")
        self.pv_button.clicked.connect(self.PVcalculate)
        self.pv_button.setEnabled(False)
        pv_layout.addWidget(self.pv_button)
        
        group_layout.addLayout(pv_layout)
        
        # Results display with scrollable area
        result_scroll = QScrollArea()
        result_scroll.setWidgetResizable(True)
        result_container = QWidget()
        result_container_layout = QVBoxLayout(result_container)
        
        self.terminal_result_label = QLabel()
        self.terminal_result_label.setWordWrap(True)
        self.terminal_result_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        result_container_layout.addWidget(self.terminal_result_label)
        
        result_scroll.setWidget(result_container)
        result_scroll.setMinimumHeight(120)
        group_layout.addWidget(result_scroll)
        
        group.setLayout(group_layout)
        parent_layout.addWidget(group)
    
    def create_fair_value_group(self, parent_layout):
        """Create the Fair Value calculation group"""
        group = QGroupBox("Fair Value Calculation")
        group_layout = QVBoxLayout()
        group_layout.setSpacing(10)
        
        # Company financials
        finance_layout = QFormLayout()
        
        self.net_cash = QDoubleSpinBox()
        self.net_cash.setRange(-999999999, 999999999)
        self.net_cash.setPrefix("Rs. ")
        self.net_cash.setValue(600.00)
        finance_layout.addRow("Net Cash (in cr.):", self.net_cash)
        
        self.shares = QDoubleSpinBox()
        self.shares.setRange(0, 999999999)
        self.shares.setSuffix(" cr.")
        self.shares.setValue(88.00)
        finance_layout.addRow("Number of Shares (in cr.):", self.shares)
        
        group_layout.addLayout(finance_layout)
        
        # Fair value calculation
        self.fair_value_button = QPushButton("Calculate Fair Value")
        self.fair_value_button.clicked.connect(self.fairValue)
        self.fair_value_button.setEnabled(False)
        group_layout.addWidget(self.fair_value_button)
        
        # Results display with scrollable area
        result_scroll = QScrollArea()
        result_scroll.setWidgetResizable(True)
        result_container = QWidget()
        result_container_layout = QVBoxLayout(result_container)
        
        self.fair_value_result_label = QLabel()
        self.fair_value_result_label.setWordWrap(True)
        self.fair_value_result_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        result_container_layout.addWidget(self.fair_value_result_label)
        
        result_scroll.setWidget(result_container)
        result_scroll.setMinimumHeight(120)
        group_layout.addWidget(result_scroll)
        
        group.setLayout(group_layout)
        parent_layout.addWidget(group)
    
    def create_button_group(self, parent_layout):
        """Create the button group for actions"""
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        self.reset_button = QPushButton("Reset All")
        self.reset_button.clicked.connect(self.reset_button_click)
        button_layout.addWidget(self.reset_button)
        
        self.save_button = QPushButton("Save Results")
        self.save_button.clicked.connect(self.save_results)
        button_layout.addWidget(self.save_button)
        
        self.exit_button = QPushButton("Exit")
        self.exit_button.clicked.connect(self.close)
        button_layout.addWidget(self.exit_button)
        
        parent_layout.addLayout(button_layout)
    
    def create_visualization_tab(self):
        """Create the visualization tab with charts"""
        vis_tab = QWidget()
        vis_layout = QVBoxLayout(vis_tab)
        
        # Chart selection
        chart_select_layout = QHBoxLayout()
        chart_select_layout.addWidget(QLabel("Select Chart:"))
        
        self.chart_selector = QComboBox()
        self.chart_selector.addItems(["Future Value Projection", "Present Value Breakdown"])
        self.chart_selector.currentIndexChanged.connect(self.update_chart)
        chart_select_layout.addWidget(self.chart_selector)
        
        self.refresh_chart_button = QPushButton("Refresh Chart")
        self.refresh_chart_button.clicked.connect(self.update_chart)
        chart_select_layout.addWidget(self.refresh_chart_button)
        
        vis_layout.addLayout(chart_select_layout)
        
        # Matplotlib figure
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        vis_layout.addWidget(self.canvas)
        
        self.tabs.addTab(vis_tab, "Visualization")
    
    def create_log_tab(self):
        """Create the log viewer tab"""
        log_tab = QWidget()
        log_layout = QVBoxLayout(log_tab)
        
        # Create scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        # Create container widget
        container = QWidget()
        container_layout = QVBoxLayout(container)
        
        self.log_viewer = QTextEdit()
        self.log_viewer.setReadOnly(True)
        container_layout.addWidget(self.log_viewer)
        
        # Add log controls
        log_control_layout = QHBoxLayout()
        
        self.refresh_log_button = QPushButton("Refresh Log")
        self.refresh_log_button.clicked.connect(self.refresh_log)
        log_control_layout.addWidget(self.refresh_log_button)
        
        self.clear_log_button = QPushButton("Clear Log")
        self.clear_log_button.clicked.connect(self.clear_log)
        log_control_layout.addWidget(self.clear_log_button)
        
        self.save_log_button = QPushButton("Save Log")
        self.save_log_button.clicked.connect(self.save_log)
        log_control_layout.addWidget(self.save_log_button)
        
        container_layout.addLayout(log_control_layout)
        
        scroll.setWidget(container)
        log_layout.addWidget(scroll)
        
        self.tabs.addTab(log_tab, "Log Viewer")
    
    def create_menu(self):
        """Create the menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        save_action = file_menu.addAction("Save Results")
        save_action.triggered.connect(self.save_results)
        
        export_action = file_menu.addAction("Export Data")
        export_action.triggered.connect(self.export_data)
        
        file_menu.addSeparator()
        
        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(self.close)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        about_action = help_menu.addAction("About")
        about_action.triggered.connect(self.show_about)
        
        docs_action = help_menu.addAction("Documentation")
        docs_action.triggered.connect(self.show_documentation)
    
    def create_status_bar(self):
        """Create the status bar"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
    
    def apply_styles(self):
        """Apply styles to the application"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QGroupBox {
                font-size: 12px;
                font-weight: bold;
                border: 1px solid #ccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 5px 10px;
                text-align: center;
                text-decoration: none;
                font-size: 12px;
                margin: 4px 2px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
            QLabel {
                font-size: 12px;
            }
            QLineEdit, QSpinBox, QDoubleSpinBox {
                padding: 3px;
                border: 1px solid #ccc;
                border-radius: 3px;
                min-width: 80px;
            }
            QTabWidget::pane {
                border: 1px solid #ccc;
                top: -1px;
            }
            QTabBar::tab {
                background: #e1e1e1;
                border: 1px solid #ccc;
                padding: 5px 10px;
            }
            QTabBar::tab:selected {
                background: #f5f5f5;
                border-bottom-color: #f5f5f5;
            }
            QScrollArea {
                border: 1px solid #ddd;
                background: white;
            }
            QTextEdit {
                font-family: Consolas, Courier New, monospace;
                font-size: 11px;
            }
        """)
    
    def FvCalculator(self):
        """Calculate future values"""
        try:
            if self.operation_future.value() <= -100:
                raise ValueError("Growth rate cannot be -100% or lower")
                
            self.list_append = []
            years = self.future_year_entry.value()
            amount = self.amount_future.value()
            growth_rate = self.operation_future.value() / 100
            
            for i in range(1, years + 1):
                formula = amount * ((1 + growth_rate) ** i)
                self.list_append.append(formula)
            
            self.sixth_term = self.list_append[-1] * 1.1
            result_text = f"Future Value Calculation completed.\nFinal year value: Rs.{self.sixth_term:.2f}"
            
            self.fv_result_label.setText(result_text)
            self.status_bar.showMessage("Future Value calculated successfully")
            logging.info(f"Future Value Calculation: {result_text}")
            
            # Enable dependent buttons
            self.npv_button.setEnabled(True)
            
        except Exception as e:
            error_msg = f"Error in Future Value calculation: {str(e)}"
            QMessageBox.critical(self, "Calculation Error", error_msg)
            logging.error(f"Future Value Calculation Error: {str(e)}")
            self.status_bar.showMessage(error_msg)
    
    def FvCalculator_b(self):
        """Calculate secondary future values"""
        try:
            if self.operation_future_b.value() <= -100:
                raise ValueError("Growth rate cannot be -100% or lower")
                
            self.list_append_b = []
            years = self.future_year_entry_b.value()
            amount = self.amount_future_b.value()
            growth_rate = self.operation_future_b.value() / 100
            
            # Include initial amount
            self.list_append_b.append(amount)
            
            for i in range(1, years + 1):
                formula = amount * ((1 + growth_rate) ** i)
                self.list_append_b.append(formula)
            
            # Remove the last duplicate
            self.list_append_b.pop()
            
            combined_values = self.list_append + self.list_append_b
            result_text = f"Secondary Future Value Calculation completed.\nAll values: {['Rs.{:.2f}'.format(x) for x in combined_values]}"
            
            self.fv_result_label.setText(self.fv_result_label.text() + "\n\n" + result_text)
            self.status_bar.showMessage("Secondary Future Value calculated successfully")
            logging.info(f"Secondary Future Value Calculation: {result_text}")
            
            # Enable dependent buttons
            self.npv_button.setEnabled(True)
            
        except Exception as e:
            error_msg = f"Error in Secondary Future Value calculation: {str(e)}"
            QMessageBox.critical(self, "Calculation Error", error_msg)
            logging.error(f"Secondary Future Value Calculation Error: {str(e)}")
            self.status_bar.showMessage(error_msg)
    
    def Nv(self):
        """Calculate net present value"""
        try:
            if not self.list_append and not self.list_append_b:
                raise ValueError("No cash flow data available")
                
            self.new_list = self.list_append + self.list_append_b
            discount_rate = self.discount_rate.value() / 100
            amount_list = []
            d = {}
            
            for i in range(len(self.new_list)):
                formula = self.new_list[i] / ((1 + discount_rate) ** (i + 1))
                amount_list.append(formula)
                d[self.new_list[i]] = formula
            
            pvvaluelist = list(d.values())
            self.sumofvalues = sum(pvvaluelist)
            
            result_text = (
                f"Net Present Value Calculation completed.\n"
                f"Discount Rate: {discount_rate*100:.1f}%\n"
                f"Present Values: {['Rs.{:.2f}'.format(x) for x in pvvaluelist]}\n"
                f"Total Present Value: Rs.{self.sumofvalues:.2f}"
            )
            
            self.npv_result_label.setText(result_text)
            self.status_bar.showMessage("NPV calculated successfully")
            logging.info(f"NPV Calculation: {result_text}")
            
            # Enable dependent buttons
            self.terminal_button.setEnabled(True)
            
        except Exception as e:
            error_msg = f"Error in NPV calculation: {str(e)}"
            QMessageBox.critical(self, "Calculation Error", error_msg)
            logging.error(f"NPV Calculation Error: {str(e)}")
            self.status_bar.showMessage(error_msg)
    
    def TerminalValue(self):
        """Calculate terminal value"""
        try:
            if not self.new_list:
                raise ValueError("No cash flow data available")
                
            fcashFlow = self.new_list[-1]
            growth_rate = self.terminal_growth.value() / 100
            discount_rate = self.discount_rate.value() / 100
            
            if growth_rate >= discount_rate:
                raise ValueError("Growth rate must be less than discount rate for terminal value calculation")
                
            self.Terminal_Value = fcashFlow * (1 + growth_rate) / (discount_rate - growth_rate)
            
            result_text = (
                f"Terminal Value Calculation completed.\n"
                f"Terminal Growth Rate: {growth_rate*100:.1f}%\n"
                f"Discount Rate: {discount_rate*100:.1f}%\n"
                f"Terminal Value: Rs.{self.Terminal_Value:.2f}"
            )
            
            self.terminal_result_label.setText(result_text)
            self.status_bar.showMessage("Terminal Value calculated successfully")
            logging.info(f"Terminal Value Calculation: {result_text}")
            
            # Enable dependent buttons
            self.pv_button.setEnabled(True)
            
        except Exception as e:
            error_msg = f"Error in Terminal Value calculation: {str(e)}"
            QMessageBox.critical(self, "Calculation Error", error_msg)
            logging.error(f"Terminal Value Calculation Error: {str(e)}")
            self.status_bar.showMessage(error_msg)
    
    def PVcalculate(self):
        """Calculate present value of terminal value"""
        try:
            if not self.new_list or self.Terminal_Value == 0:
                raise ValueError("No terminal value available for calculation")
                
            discount_rate = self.discount_rate.value() / 100
            self.formula = self.Terminal_Value / ((1 + discount_rate) ** len(self.new_list))
            
            result_text = f"Present Value of Terminal Value: Rs.{self.formula:.2f}"
            
            self.terminal_result_label.setText(
                self.terminal_result_label.text() + "\n\n" + result_text
            )
            self.status_bar.showMessage("PV of Terminal Value calculated successfully")
            logging.info(f"PV of Terminal Value: {result_text}")
            
            # Enable dependent buttons
            self.fair_value_button.setEnabled(True)
            
        except Exception as e:
            error_msg = f"Error in PV calculation: {str(e)}"
            QMessageBox.critical(self, "Calculation Error", error_msg)
            logging.error(f"PV Calculation Error: {str(e)}")
            self.status_bar.showMessage(error_msg)
    
    def fairValue(self):
        """Calculate fair value"""
        try:
            self.netcash = self.net_cash.value()
            self.totalShare = self.shares.value()
            
            if self.totalShare <= 0:
                raise ValueError("Number of shares must be positive")
                
            valuation = self.formula + self.sumofvalues + self.netcash
            FairValue = valuation / self.totalShare
            
            possibleValuemin = FairValue * (1 - 0.1)
            possibleValuemax = FairValue * (1 + 0.1)
            
            result_text = (
                f"Fair Value Calculation completed.\n"
                f"Valuation: Rs.{valuation:.2f}\n"
                f"Number of Shares: {self.totalShare:.2f} cr.\n"
                f"Fair Value per Share: Rs.{FairValue:.2f}\n"
                f"Possible Valuation Range: Rs.{possibleValuemin:.2f} to Rs.{possibleValuemax:.2f}"
            )
            
            self.fair_value_result_label.setText(result_text)
            self.status_bar.showMessage("Fair Value calculated successfully")
            logging.info(f"Fair Value Calculation: {result_text}")
            
            # Update chart with the new data
            self.update_chart()
            
        except Exception as e:
            error_msg = f"Error in Fair Value calculation: {str(e)}"
            QMessageBox.critical(self, "Calculation Error", error_msg)
            logging.error(f"Fair Value Calculation Error: {str(e)}")
            self.status_bar.showMessage(error_msg)
    
    def update_chart(self):
        """Update the visualization chart based on current data"""
        try:
            self.figure.clear()
            chart_type = self.chart_selector.currentText()
            
            if chart_type == "Future Value Projection" and self.list_append:
                ax = self.figure.add_subplot(111)
                years = list(range(1, len(self.list_append) + 1))
                ax.plot(years, self.list_append, 'b-', label='Primary CF')
                
                if self.list_append_b:
                    years_b = list(range(len(self.list_append) + 1, 
                                      len(self.list_append) + len(self.list_append_b) + 1))
                    ax.plot(years_b, self.list_append_b, 'g-', label='Secondary CF')
                
                ax.set_title('Future Cash Flow Projection')
                ax.set_xlabel('Year')
                ax.set_ylabel('Value (Rs.)')
                ax.legend()
                ax.grid(True)
                
            elif chart_type == "Present Value Breakdown" and self.new_list:
                ax = self.figure.add_subplot(111)
                labels = ['PV of Cash Flows', 'PV of Terminal Value', 'Net Cash']
                sizes = [self.sumofvalues, self.formula, self.netcash]
                
                # Only include positive values
                filtered_labels = []
                filtered_sizes = []
                for label, size in zip(labels, sizes):
                    if size > 0:
                        filtered_labels.append(label)
                        filtered_sizes.append(size)
                
                if filtered_sizes:
                    ax.pie(filtered_sizes, labels=filtered_labels, autopct='%1.1f%%',
                          startangle=90)
                    ax.axis('equal')  # Equal aspect ratio ensures pie is drawn as a circle
                    ax.set_title('Valuation Components Breakdown')
                else:
                    ax.text(0.5, 0.5, 'No positive values to display', 
                           ha='center', va='center')
            
            self.canvas.draw()
            self.status_bar.showMessage(f"Chart updated: {chart_type}")
            
        except Exception as e:
            logging.error(f"Chart Update Error: {str(e)}")
            self.status_bar.showMessage("Error updating chart. Check data availability.")
    
    def reset_button_click(self):
        """Reset all inputs and calculations"""
        try:
            # Reset input fields
            self.amount_future.setValue(80.00)
            self.operation_future.setValue(15.00)
            self.future_year_entry.setValue(5)
            self.amount_future_b.setValue(117.00)
            self.operation_future_b.setValue(8.00)
            self.future_year_entry_b.setValue(5)
            self.net_cash.setValue(600.00)
            self.shares.setValue(88.00)
            self.discount_rate.setValue(9.0)
            self.terminal_growth.setValue(3.5)
            
            # Reset result labels
            self.fv_result_label.clear()
            self.npv_result_label.clear()
            self.terminal_result_label.clear()
            self.fair_value_result_label.clear()
            
            # Reset variables
            self.list_append = []
            self.list_append_b = []
            self.sixth_term = 0
            self.new_list = []
            self.sumofvalues = 0
            self.Terminal_Value = 0
            self.formula = 0
            self.netcash = 0
            self.totalShare = 0
            
            # Disable dependent buttons
            self.npv_button.setEnabled(False)
            self.terminal_button.setEnabled(False)
            self.pv_button.setEnabled(False)
            self.fair_value_button.setEnabled(False)
            
            # Update chart
            self.update_chart()
            
            self.status_bar.showMessage("All inputs and results reset")
            logging.info("Application reset")
            
        except Exception as e:
            logging.error(f"Reset Error: {str(e)}")
            self.status_bar.showMessage("Error during reset")
    
    def save_results(self):
        """Save calculation results to a file"""
        try:
            options = QFileDialog.Option(0)
            file_name, _ = QFileDialog.getSaveFileName(
                self, "Save Results", "", "Text Files (*.txt);;All Files (*)", options=options
            )
            
            if file_name:
                with open(file_name, 'w', encoding='utf-8') as file:
                    file.write("Financial Calculator Results\n")
                    file.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                    
                    if self.fv_result_label.text():
                        file.write("Future Value Calculations:\n")
                        file.write(self.fv_result_label.text() + "\n\n")
                    
                    if self.npv_result_label.text():
                        file.write("NPV Calculations:\n")
                        file.write(self.npv_result_label.text() + "\n\n")
                    
                    if self.terminal_result_label.text():
                        file.write("Terminal Value Calculations:\n")
                        file.write(self.terminal_result_label.text() + "\n\n")
                    
                    if self.fair_value_result_label.text():
                        file.write("Fair Value Calculations:\n")
                        file.write(self.fair_value_result_label.text() + "\n\n")
                
                self.status_bar.showMessage(f"Results saved to {file_name}")
                logging.info(f"Results saved to {file_name}")
                
        except Exception as e:
            error_msg = f"Error saving results: {str(e)}"
            QMessageBox.critical(self, "Save Error", error_msg)
            logging.error(error_msg)
            self.status_bar.showMessage("Error saving results")
    
    def export_data(self):
        """Export calculation data to CSV"""
        try:
            if not self.new_list:
                raise ValueError("No data available for export")
                
            options = QFileDialog.Option(0)
            file_name, _ = QFileDialog.getSaveFileName(
                self, "Export Data", "", "CSV Files (*.csv);;All Files (*)", options=options
            )
            
            if file_name:
                with open(file_name, 'w', encoding='utf-8') as file:
                    file.write("Year,Primary CF,Secondary CF\n")
                    
                    max_years = max(len(self.list_append), len(self.list_append_b))
                    for year in range(1, max_years + 1):
                        primary = self.list_append[year-1] if year <= len(self.list_append) else ""
                        secondary = self.list_append_b[year-1] if year <= len(self.list_append_b) else ""
                        file.write(f"{year},{primary},{secondary}\n")
                
                self.status_bar.showMessage(f"Data exported to {file_name}")
                logging.info(f"Data exported to {file_name}")
                
        except Exception as e:
            error_msg = f"Error exporting data: {str(e)}"
            QMessageBox.critical(self, "Export Error", error_msg)
            logging.error(error_msg)
            self.status_bar.showMessage("Error exporting data")
    
    def refresh_log(self):
        """Refresh the log viewer with current log file contents"""
        try:
            with open('financial_calculator.log', 'r', encoding='utf-8') as log_file:
                self.log_viewer.setPlainText(log_file.read())
            
            self.log_viewer.verticalScrollBar().setValue(
                self.log_viewer.verticalScrollBar().maximum()
            )
            self.status_bar.showMessage("Log refreshed")
            
        except Exception as e:
            self.log_viewer.setPlainText(f"Error reading log file: {str(e)}")
            logging.error(f"Log Refresh Error: {str(e)}")
            self.status_bar.showMessage("Error refreshing log")
    
    def clear_log(self):
        """Clear the log file"""
        try:
            with open('financial_calculator.log', 'w', encoding='utf-8'):
                pass
            self.log_viewer.clear()
            self.status_bar.showMessage("Log cleared")
            logging.info("Log file cleared by user")
            
        except Exception as e:
            error_msg = f"Error clearing log: {str(e)}"
            self.log_viewer.setPlainText(error_msg)
            logging.error(error_msg)
            self.status_bar.showMessage("Error clearing log")
    
    def save_log(self):
        """Save the log to a different file"""
        try:
            options = QFileDialog.Option(0)
            file_name, _ = QFileDialog.getSaveFileName(
                self, "Save Log", "", "Log Files (*.log);;Text Files (*.txt);;All Files (*)", 
                options=options
            )
            
            if file_name:
                with open('financial_calculator.log', 'r', encoding='utf-8') as source, open(file_name, 'w', encoding='utf-8') as target:
                    target.write(source.read())
                
                self.status_bar.showMessage(f"Log saved to {file_name}")
                logging.info(f"Log saved to {file_name}")
                
        except Exception as e:
            error_msg = f"Error saving log: {str(e)}"

    def show_about(self):
        """Show about dialog"""
        about_text = (
            "Professional Financial Calculator\n"
            "Version 1.0\n\n"
            "A comprehensive tool for financial valuation calculations including:\n"
            "- Future Value projections\n"
            "- Net Present Value calculations\n"
            "- Terminal Value estimation\n"
            "- Fair Value determination\n\n"
            "© 2023 Financial Tools Inc."
        )
        QMessageBox.about(self, "About Financial Calculator", about_text)
        logging.info("About dialog displayed")
         
    def show_documentation(self):
        """Show documentation"""
        doc_text = (
            "Financial Calculator Documentation\n\n"
            "1. Future Value Calculations:\n"
            "   - Enter the initial cash flow amount, growth rate, and number of years\n"
            "   - For secondary cash flows, use the second set of inputs\n\n"
            "2. Net Present Value:\n"
            "   - Calculates present value of future cash flows using discount rate\n\n"
            "3. Terminal Value:\n"
            "   - Estimates perpetual value beyond projection period\n\n"
            "4. Fair Value:\n"
            "   - Combines all components to estimate fair value per share\n\n"
            "Visualizations are available in the Visualization tab."
        )
        QMessageBox.information(self, "Documentation", doc_text)
        logging.info("Documentation displayed")
    



if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Set application icon
    try:
        app.setWindowIcon(QIcon('calculator.png'))
    except:
        pass
    
    calculator = FinancialCalculator()
    calculator.show()
    sys.exit(app.exec())

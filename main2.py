import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QAction, QVBoxLayout, QWidget,
    QPushButton, QLabel, QLineEdit, QFileDialog, QTabWidget, QTextEdit,
    QHBoxLayout, QStackedWidget, QComboBox, QDoubleSpinBox, QSpinBox,
    QStatusBar, QMessageBox, QProgressBar, QFrame, QGridLayout, QScrollArea,
    QCheckBox, QGroupBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSize
from PyQt5.QtGui import QPixmap, QIcon, QFont, QColor
import cv2
import torch
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class BlueberryDetectionSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("蓝莓目标检测系统")
        self.setGeometry(100, 100, 1400, 900)
        self.setWindowIcon(QIcon(self.resource_path('icons/blueberry.jpg')))

        # Define a more cohesive color palette
        self.primary_color = QColor("#E2EAF4")  # A brighter, more appealing green
        self.secondary_color = QColor("#388E3C") # A darker shade of green for highlights
        self.background_color = QColor("#F5F5F5")  # 背景颜色
        self.widget_background_color = QColor("white")
        self.text_color = QColor("#212121")  # Darker text for better readability
        self.disabled_color = QColor("#BDBDBD") # For disabled widgets

        # Set application-wide font
        self.base_font = QFont("微软雅黑", 10) # Use a more common and modern font
        QApplication.instance().setFont(self.base_font)

        # Main window layout
        self.central_widget = QWidget()
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)
        self.setStyleSheet(f"background-color: {self.background_color.name()}")

        # # Top buttons layout
        # self.top_buttons_widget = QWidget()
        # self.top_buttons_layout = QHBoxLayout()
        # self.top_buttons_layout.setContentsMargins(20, 10, 20, 10)
        # self.top_buttons_widget.setLayout(self.top_buttons_layout)
        # self.main_layout.addWidget(self.top_buttons_widget)

        # 修改顶部按钮区域的样式
        self.top_buttons_widget = QWidget()
        self.top_buttons_layout = QHBoxLayout()
        # 减小上下边距，让背景色区域更紧凑
        self.top_buttons_layout.setContentsMargins(20, 10, 20, 10)
        self.top_buttons_layout.setSpacing(20)
        self.top_buttons_widget.setLayout(self.top_buttons_layout)

        # 设置整个顶部区域的背景色
        self.top_buttons_widget.setStyleSheet("""
                QWidget {
                    background-color: #CDD4DA;  /* 深色背景 */
                    border-bottom: 2px solid #CDD4DA;
                }
            """)
        self.main_layout.addWidget(self.top_buttons_widget)

        # Create top buttons
        self.btn_data_collection = self.create_top_button("数据采集", "data", lambda: self.switch_page(0))
        self.top_buttons_layout.addWidget(self.btn_data_collection)
        self.btn_model_training = self.create_top_button("模型训练", "model", lambda: self.switch_page(1))
        self.top_buttons_layout.addWidget(self.btn_model_training)
        self.btn_image_detection = self.create_top_button("图像检测", "detect", lambda: self.switch_page(2))
        self.top_buttons_layout.addWidget(self.btn_image_detection)
        self.btn_result_statistics = self.create_top_button("结果统计", "stats", lambda: self.switch_page(3))
        self.top_buttons_layout.addWidget(self.btn_result_statistics)

        # # Add a horizontal line separator
        # self.separator = QFrame()
        # self.separator.setFrameShape(QFrame.HLine)
        # self.separator.setFrameShadow(QFrame.Sunken)
        # self.separator.setStyleSheet("QFrame { margin: 10px 0; }") # Keep it simple
        # self.main_layout.addWidget(self.separator)

        # Stacked widget for content pages
        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)

        # Create and add pages to stacked widget
        self.data_collection_page = self.create_data_collection_page()
        self.stacked_widget.addWidget(self.data_collection_page)

        self.model_training_page = self.create_model_training_page()
        self.stacked_widget.addWidget(self.model_training_page)

        self.image_detection_page = self.create_image_detection_page()
        self.stacked_widget.addWidget(self.image_detection_page)

        self.result_statistics_page = self.create_result_statistics_page()
        self.stacked_widget.addWidget(self.result_statistics_page)

        # Initialize menu
        self.init_menu()
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.setStyleSheet(f"QStatusBar {{ color: white; background-color: "
                                      f"{self.text_color.name()}; font-size: 10pt }}")

        # Style the widgets
        self.style_widgets()

        # Store selected data in variables
        self.selected_preprocess_folder = ""
        self.selected_save_folder = ""
        self.selected_weights_file = ""
        self.selected_image_path = ""
        self.training_history = {"loss": [], "accuracy": []}

    def style_widgets(self):
        # Style for QFrame group boxes
        self.setStyleSheet("""
            QFrame {
                border: 1px solid #BDBDBD;
                border-radius: 5px;
                background-color: white;
            }
            QLabel {
                color: #333;
            }
            QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {
                border: 1px solid #ccc;
                border-radius: 3px;
                padding: 5px;
                background-color: white;
                selection-background-color: #0859E4;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #43A047;
            }
            QPushButton:pressed {
                background-color: #388E3C;
            }
            QPushButton:disabled {
                background-color: #BDBDBD;
                color: #616161;
            }
            QProgressBar {
                border: 1px solid #ccc;
                border-radius: 5px;
                text-align: center;
                background-color: #EEEEEE;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
            }
        """)

    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, "data", relative_path)

    def init_menu(self):
        menu_bar = self.menuBar()

        # File menu
        file_menu = menu_bar.addMenu("文件")
        open_action = QAction(QIcon(self.resource_path("icons/1.jpg")), "打开", self)
        save_action = QAction(QIcon(self.resource_path("icons/1.jpg")), "保存", self)
        exit_action = QAction(QIcon(self.resource_path("icons/1.jpg")), "退出", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(exit_action)

        # Help menu
        help_menu = menu_bar.addMenu("帮助")
        about_action = QAction(QIcon(self.resource_path("icons/1.jpg")), "关于", self)
        help_menu.addAction(about_action)

    def create_top_button(self, text, icon_name, callback):
        button = QPushButton(text)
        button.clicked.connect(callback)
        button.setIcon(QIcon(self.resource_path(f"icons/{icon_name}.jpg")))
        button.setIconSize(QSize(20,20))
        # button.setFont(QFont(self.base_font.family(), 120))
        # 修改字体大小
        font = QFont(self.base_font.family(), 18)  # 改为14号字体
        font.setBold(True)  # 设置为粗体
        button.setFont(font)

        button.setMinimumWidth(150)
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.primary_color.name()};
                color: black;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 25px;
            }}
            QPushButton:hover {{
                background-color: {self.secondary_color.name()};
                color: white;
            }}
        """)
        return button

    def create_button(self, text, callback, icon_name=None):
        button = QPushButton(text)
        button.clicked.connect(callback)
        button.setFont(self.base_font)
        if icon_name:
            button.setIcon(QIcon(self.resource_path(f"icons/{icon_name}.jpg")))
            button.setIconSize(QSize(20, 20))
        button.setMinimumWidth(80)
        button.setMaximumWidth(200)
        button.setStyleSheet("""
            QPushButton {
                background-color: #E2EAF4;
                color: black;
                border: none;
                border-radius: 5px;
                padding: 12px 12px;
            }
            QPushButton:hover {
                background-color: #43A047;
                color: white;
            }
            QPushButton:pressed {
                background-color: #388E3C;
            }
        """)
        return button

    def create_label(self, text, bold=False, size=10):
        label = QLabel(text)
        font = QFont(self.base_font.family(), size)
        if bold:
            font.setBold(True)
        label.setFont(font)
        label.setStyleSheet(f"color: {self.text_color.name()};")
        return label

    def switch_page(self, index):
        self.stacked_widget.setCurrentIndex(index)

    def create_data_collection_page(self):
        page = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # title = self.create_label("数据采集", bold=True, size=16)
        # title.setAlignment(Qt.AlignCenter)
        # layout.addWidget(title)

        group_box = QFrame()
        group_box_layout = QVBoxLayout(group_box)
        group_box.setContentsMargins(10, 10, 10, 10)
        layout.addWidget(group_box)

        preprocess_label = self.create_label("蓝莓图像预处理：", bold=True)
        group_box_layout.addWidget(preprocess_label)
        preprocess_layout = QHBoxLayout()
        self.preprocess_folder_line = QLineEdit()
        preprocess_layout.addWidget(self.preprocess_folder_line)
        preprocess_button = self.create_button("选择图像文件夹", self.select_preprocess_folder, "folder")
        preprocess_layout.addWidget(preprocess_button)
        group_box_layout.addLayout(preprocess_layout)
        preprocess_images_button = self.create_button("预处理图像", self.preprocess_images, "process")
        group_box_layout.addWidget(preprocess_images_button, alignment = Qt.AlignRight)

        split_label = self.create_label("图像数据划分：", bold=True)
        group_box_layout.addWidget(split_label)
        split_layout = QHBoxLayout()
        split_layout.addWidget(self.create_label("划分比例 (训练集):"))
        self.split_ratio_spin = QDoubleSpinBox()
        self.split_ratio_spin.setRange(0.1, 0.9)
        self.split_ratio_spin.setValue(0.5)
        self.split_ratio_spin.setSingleStep(0.01)  # 设置步长为0.01
        self.split_ratio_spin.setDecimals(2)  # 显示2位小数
        self.split_ratio_spin.setFixedHeight(25)  # 保持高度设置
        # self.split_ratio_spin.setFixedWidth(70)  # 增加宽度到70像素
        self.split_ratio_spin.setFixedHeight(50)  # 增加整体高度

        # 可以添加样式使其看起来更美观
        self.split_ratio_spin.setStyleSheet("""
            QDoubleSpinBox {
                padding: 2px 5px;
                border: 1px solid #BDBDBD;
                border-radius: 3px;
                background-color: white;
            }
            QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {
                width: 30px;
            }
        """)

        split_layout.addWidget(self.split_ratio_spin)
        split_button = self.create_button("划分数据集", self.split_data, "split")
        split_layout.addWidget(split_button)
        group_box_layout.addLayout(split_layout)

        save_label = self.create_label("图像数据存储：", bold=True)
        group_box_layout.addWidget(save_label)
        save_layout = QHBoxLayout()
        self.save_folder_line = QLineEdit()
        save_layout.addWidget(self.save_folder_line)
        save_button = self.create_button("选择存储目录", self.select_save_folder, "folder")
        save_layout.addWidget(save_button)
        save_dataset_button = self.create_button("存储数据集", self.save_data, "save")
        save_layout.addWidget(save_dataset_button)
        group_box_layout.addLayout(save_layout)

        group_box.setStyleSheet(f"QFrame {{ border: 1px solid {self.disabled_color.name()}; border-radius: 5px; background-color: {self.widget_background_color.name()}; padding: 10px; }}")

        page.setLayout(layout)
        return page

    def create_model_training_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title = self.create_label("模型训练", bold=True, size=16)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        group_box = QFrame()
        group_box_layout = QVBoxLayout(group_box)
        group_box.setContentsMargins(10, 10, 10, 10)
        layout.addWidget(group_box)

        weights_label = self.create_label("预训练权重加载：", bold=True)
        group_box_layout.addWidget(weights_label)
        weights_layout = QHBoxLayout()
        self.weights_file_line = QLineEdit()
        weights_layout.addWidget(self.weights_file_line)
        weights_button = self.create_button("加载预训练权重", self.load_weights, "upload")
        weights_layout.addWidget(weights_button)
        group_box_layout.addLayout(weights_layout)

        params_label = self.create_label("训练参数设置：", bold=True)
        group_box_layout.addWidget(params_label)
        params_layout = QGridLayout()
        params_layout.setSpacing(10)
        params_layout.addWidget(self.create_label("学习率:"), 0, 0)
        self.lr_spin = QDoubleSpinBox()
        self.lr_spin.setRange(0, 1)
        self.lr_spin.setValue(0.5)
        self.lr_spin.setSingleStep(0.01)
        self.lr_spin.setDecimals(2)
        params_layout.addWidget(self.lr_spin, 0, 1)

        params_layout.addWidget(self.create_label("批量大小:"), 1, 0)
        self.batch_size_spin = QSpinBox()
        self.batch_size_spin.setRange(1, 64)
        self.batch_size_spin.setValue(16)
        params_layout.addWidget(self.batch_size_spin, 1, 1)

        params_layout.addWidget(self.create_label("epochs:"), 2, 0)
        self.epochs_spin = QSpinBox()
        self.epochs_spin.setRange(1, 100)
        self.epochs_spin.setValue(10)
        params_layout.addWidget(self.epochs_spin, 2, 1)
        group_box_layout.addLayout(params_layout)

        strategy_label = self.create_label("模型训练策略设置：", bold=True)
        group_box_layout.addWidget(strategy_label)
        strategy_layout = QHBoxLayout()
        strategy_layout.addWidget(self.create_label("优化器:"))
        self.optimizer_combo = QComboBox()
        self.optimizer_combo.addItems(["SGD", "Adam"])
        strategy_layout.addWidget(self.optimizer_combo)
        strategy_layout.addWidget(self.create_label("损失函数:"))
        self.loss_combo = QComboBox()
        self.loss_combo.addItems(["CrossEntropy", "MSE"])
        strategy_layout.addWidget(self.loss_combo)
        confirm_strategy_button = self.create_button("确认策略", self.confirm_training_strategy, "confirm")
        strategy_layout.addWidget(confirm_strategy_button)
        group_box_layout.addLayout(strategy_layout)

        self.train_progress = QProgressBar()
        group_box_layout.addWidget(self.train_progress)
        train_button = self.create_button("开始训练", self.start_training, "start")
        group_box_layout.addWidget(train_button, alignment = Qt.AlignCenter)

        # training monitoring plot
        self.training_canvas = FigureCanvas(plt.Figure(figsize=(5,3)))
        group_box_layout.addWidget(self.training_canvas)
        group_box_layout.setStretch(5, 2)

        group_box.setStyleSheet(f"QFrame {{ border: 1px solid {self.disabled_color.name()}; "
                                f"border-radius: 5px; background-color: {self.widget_background_color.name()}; "
                                f"padding: 10px; }}")

        page.setLayout(layout)
        return page

    def create_image_detection_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title = self.create_label("蓝莓图像检测", bold=True, size=16)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        group_box = QFrame()
        group_box_layout = QVBoxLayout(group_box)
        group_box.setContentsMargins(10, 10, 10, 10)
        layout.addWidget(group_box)

        import_label = self.create_label("图像导入：", bold=True)
        group_box_layout.addWidget(import_label)
        import_layout = QHBoxLayout()
        self.image_path_line = QLineEdit()
        import_layout.addWidget(self.image_path_line)
        import_button = self.create_button("导入图像", self.select_image, "image")
        import_layout.addWidget(import_button)
        group_box_layout.addLayout(import_layout)

        self.image_display = QLabel()
        self.image_display.setFixedSize(600, 400)
        self.image_display.setStyleSheet("QLabel { border: 1px solid #ccc; border-radius: 5px; background-color: white; alignment: center; }")
        self.image_display.setAlignment(Qt.AlignCenter)
        group_box_layout.addWidget(self.image_display)

        output_label = self.create_label("检测结果输出与校正：", bold=True)
        group_box_layout.addWidget(output_label)
        output_layout = QHBoxLayout()
        detect_button = self.create_button("检测图像", self.detect_image, "detect")
        output_layout.addWidget(detect_button)
        save_result_button = self.create_button("保存结果", self.save_detection_result, "save")
        output_layout.addWidget(save_result_button)
        group_box_layout.addLayout(output_layout)

        group_box.setStyleSheet(f"QFrame {{ border: 1px solid {self.disabled_color.name()}; border-radius: 5px; background-color: {self.widget_background_color.name()}; padding: 10px; }}")

        page.setLayout(layout)
        return page

    def create_result_statistics_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title = self.create_label("结果统计", bold=True, size=16)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        group_box = QFrame()
        group_box_layout = QVBoxLayout(group_box)
        group_box.setContentsMargins(10, 10, 10, 10)
        layout.addWidget(group_box)

        count_label = self.create_label("数量统计：", bold=True)
        group_box_layout.addWidget(count_label)
        self.count_display = QLabel("数量: 0")
        self.count_display.setStyleSheet(f"QLabel {{ background-color: {self.widget_background_color.name()}; padding: 5px; border-radius: 3px; border: 1px solid #ccc; }}")
        group_box_layout.addWidget(self.count_display)

        error_label = self.create_label("检测误差统计：", bold=True)
        group_box_layout.addWidget(error_label)
        self.error_display = QTextEdit()
        self.error_display.setStyleSheet(f"QTextEdit {{ background-color: {self.widget_background_color.name()}; border: 1px solid #ccc; border-radius: 3px; }}")
        self.error_display.setReadOnly(True)
        group_box_layout.addWidget(self.error_display)

        calculate_button = self.create_button("计算统计信息", self.calculate_statistics, "calculate")
        group_box_layout.addWidget(calculate_button)

        group_box.setStyleSheet(f"QFrame {{ border: 1px solid {self.disabled_color.name()}; border-radius: 5px; background-color: {self.widget_background_color.name()}; padding: 10px; }}")

        page.setLayout(layout)
        return page

    def select_preprocess_folder(self):
         folder = QFileDialog.getExistingDirectory(self, "选择预处理文件夹")
         if folder:
            self.preprocess_folder_line.setText(folder)
            self.selected_preprocess_folder = folder

    def preprocess_images(self):
        if not self.selected_preprocess_folder:
            QMessageBox.warning(self, "警告", "请选择预处理文件夹")
            return
        self.status_bar.showMessage("图像预处理完成")

    def split_data(self):
         if not self.selected_preprocess_folder:
             QMessageBox.warning(self, "警告", "请选择预处理文件夹")
             return
         ratio = self.split_ratio_spin.value()
         self.status_bar.showMessage(f"数据集划分完成，训练集比例: {ratio}")

    def select_save_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "选择存储目录")
        if folder:
            self.save_folder_line.setText(folder)
            self.selected_save_folder = folder

    def save_data(self):
        if not self.selected_save_folder:
            QMessageBox.warning(self, "警告", "请选择存储目录")
            return
        self.status_bar.showMessage("数据集存储完成")

    def load_weights(self):
        file, _ = QFileDialog.getOpenFileName(self, "加载预训练权重", "", "权重文件 (*.pth)")
        if file:
             self.weights_file_line.setText(file)
             self.selected_weights_file = file

    def confirm_training_strategy(self):
        optimizer = self.optimizer_combo.currentText()
        loss_fn = self.loss_combo.currentText()
        self.status_bar.showMessage(f"训练策略设置完成，优化器: {optimizer}, 损失函数: {loss_fn}")

    def start_training(self):
         if not self.selected_weights_file:
             QMessageBox.warning(self, "警告", "请加载预训练权重")
             return
         # Simulate training progress
         self.train_progress.setValue(0)
         self.status_bar.showMessage("训练开始")
         self.training_history = {"loss": [], "accuracy": []}
         training_thread = TrainingThread(epochs=self.epochs_spin.value(),
                                    lr = self.lr_spin.value(),
                                    batch_size = self.batch_size_spin.value())
         training_thread.progress_update.connect(self.update_training_progress)
         training_thread.finished.connect(self.training_finished)
         training_thread.start()

    def update_training_progress(self, progress, loss, accuracy):
        self.train_progress.setValue(progress)
        self.training_history["loss"].append(loss)
        self.training_history["accuracy"].append(accuracy)
        self.update_training_plot()

    def update_training_plot(self):
         self.training_canvas.figure.clear()
         ax = self.training_canvas.figure.add_subplot(111)
         ax.plot(self.training_history["loss"], label="Loss")
         ax.plot(self.training_history["accuracy"], label="Accuracy")
         ax.set_title("Training Progress")
         ax.set_xlabel("Epochs")
         ax.set_ylabel("Value")
         ax.legend()
         self.training_canvas.draw()

    def training_finished(self):
        self.status_bar.showMessage("训练完成")

    def select_image(self):
        file, _ = QFileDialog.getOpenFileName(self, "导入图像", "", "Images (*.png *.jpg *.jpeg)")
        if file:
            self.image_path_line.setText(file)
            self.selected_image_path = file
            pixmap = QPixmap(file)
            pixmap = pixmap.scaled(self.image_display.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_display.setPixmap(pixmap)

    def detect_image(self):
        if not self.selected_image_path:
            QMessageBox.warning(self, "警告", "请选择图像")
            return
        # Implement image detection logic here
        self.status_bar.showMessage("图像检测完成")
        # Display detection result on image_display

    def save_detection_result(self):
         # Implement result saving logic here
        self.status_bar.showMessage("检测结果已保存")

    def calculate_statistics(self):
        # Implement count calculation logic here
        self.count_display.setText("数量: 100")  # Example value
        # Implement error calculation logic here
        self.error_display.setText("准确率: 95%\n精度: 90%")  # Example values

class TrainingThread(QThread):
    progress_update = pyqtSignal(int, float, float)
    finished = pyqtSignal()

    def __init__(self, epochs=10, lr=0.001, batch_size=16):
       super().__init__()
       self.epochs = epochs
       self.lr = lr
       self.batch_size = batch_size

    def run(self):
        for epoch in range(self.epochs):
             loss = np.random.uniform(0.1, 1)
             accuracy = np.random.uniform(0.6, 0.95)
             progress = (epoch + 1) * 100 // self.epochs
             self.progress_update.emit(progress, loss, accuracy)
             QThread.msleep(300)

        self.finished.emit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BlueberryDetectionSystem()
    window.show()
    sys.exit(app.exec_())
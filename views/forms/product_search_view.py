from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from data.data_classes import ProductItem
from views.theme import Theme
from views.items.product_card_item import ProductCardItem
import os.path


class ProductSearchView(QWidget):
    def __init__(self, parent=None) -> None:
        QWidget.__init__(self, parent)
        self.set_styleSheet("page_widget_theme.qss")

        self.current_filter = "id"

        header_product_search = QLabel("Product Search", self)
        header_product_search.setFont(Theme.POPPINS_BOLD_24)
        header_product_search.setObjectName("h1")
        header_product_search.setGeometry(53, 32, 190, 36)

        self.product_search_input = QLineEdit(self)
        self.product_search_input.setGeometry(53, 76, 680, 40)
        self.product_search_input.setFont(Theme.POPPINS_REGULAR_14)

        self.product_search_button = QPushButton("SEARCH", self)
        self.product_search_button.setFont(Theme.POPPINS_BOLD_18)
        self.product_search_button.setObjectName("yellow_btn")
        self.product_search_button.setGeometry(613, 127, 120, 40)

        option = QWidget(self)
        option.setObjectName("option")
        option.setGeometry(53, 146, 368, 21)
        option.setStyleSheet("")
        option_layout = QHBoxLayout(option)
        option_layout.setContentsMargins(0, 0, 0, 0)
        self.filter_id = QRadioButton("ID")
        self.filter_id.setFixedWidth(45)
        self.filter_id.setFont(Theme.POPPINS_BOLD_14)

        self.filter_product_name = QRadioButton("Product Name")
        self.filter_product_name.setFixedWidth(130)
        self.filter_product_name.setFont(Theme.POPPINS_BOLD_14)

        self.filter_customer_name = QRadioButton("Customer Name")
        self.filter_customer_name.setFont(Theme.POPPINS_BOLD_14)
        option_layout.addWidget(self.filter_id)
        option_layout.addWidget(self.filter_product_name)
        option_layout.addWidget(self.filter_customer_name)

        # UI
        ui_linebreak = QLabel(self)
        ui_linebreak.setObjectName("linebreak_top")
        ui_linebreak.setGeometry(53, 198, 680, 1)

        ui_guide = QLabel(
            "Enter quantity to add or export products", self)
        ui_guide.setFont(Theme.POPPINS_REGULAR_14)
        ui_guide.setAlignment(Qt.AlignCenter)
        ui_guide.setGeometry(243, 187, 300, 21)
        ui_guide.setObjectName("guide")

        ui_img = QLabel(self)
        ui_img.setGeometry(250, 32, 30, 30)
        ui_img.setStyleSheet("background-color: none;")
        img = QPixmap(f":/icons/search.svg").scaled(30, 30)
        img = img.transformed(QTransform().scale(-1, 1))
        painter = QPainter(img)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(img.rect(), QColor("#406882"))
        painter.end()
        ui_img.setPixmap(img)

        scroll_area = QScrollArea(self)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setWidgetResizable(True)
        scroll_area.setGeometry(53, 222, 699, 520)
        self.scroll_area_widget = QWidget()
        self.scroll_area_widget.setObjectName("scroll_area")
        self.scroll_area_layout = QVBoxLayout(self.scroll_area_widget)
        self.scroll_area_layout.setSpacing(10)
        self.scroll_area_layout.setContentsMargins(0, 10, 20, 10)
        scroll_area.setWidget(self.scroll_area_widget)
        self.spacer = QSpacerItem(
            0, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

    def add_product_card(self, product_item: ProductItem) -> None:
        """Add product card on Product search window"""
        self.scroll_area_layout.removeItem(self.spacer)
        # card = ProductSearchCardController(product_item).get_view()
        # self.scroll_area_layout.addWidget(card)
        item_container = QWidget(self)
        item_container.setFixedSize(680, 150)
        item_container.setStyleSheet(
            "background-color: #F8F8FF; border-radius: 25px")
        item = ProductCardItem(item_container, product_item)
        self.scroll_area_layout.addWidget(item_container)
        self.scroll_area_layout.addItem(self.spacer)

    def clear_product_card(self) -> None:
        childs = self.scroll_area_widget.children()
        if len(childs) > 1:
            childs = childs[1:]
            for widget in childs:
                widget.close()

    def get_filter(self) -> str:
        if self.filter_customer_name.isChecked():
            return "customer name"
        elif self.filter_product_name.isChecked():
            return "product name"
        elif self.filter_id.isChecked():
            return "id"
        else:
            return "None"

    def get_search_input(self) -> str:
        return self.product_search_input.text()

    def set_search_bt_listener(self, function) -> None:
        self.product_search_button.clicked.connect(function)

    def set_styleSheet(self, file_name) -> None:
        file_path = os.path.dirname(os.path.abspath(__file__))
        real_path = os.path.join(file_path, file_name)
        with open(real_path, 'r') as f:
            style = f.read()
            self.setStyleSheet(style)
        f.close()

import random
import re
import sys
import uuid
import json
from datetime import datetime
import random
from dataclasses import dataclass
from unittest import result

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt

from extras import normalize_string

@dataclass
class ButtonConfig:
    name: str
    text: str
    func: callable
    enabled: bool = False

class App(QWidget):

    def __init__(self):
        super().__init__()
        # windows
        self.setWindowTitle("PPR QA Assistant")
        self.setGeometry(100, 100, 800, 350)
        # attrs
        self.return_packages_array = []

        self.setStyleSheet(self.dark_style())

        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        # --- LEFT SIDE ---
        left_layout = QVBoxLayout()
        self.entries = {}

        fields = [
            ("packages", "Идентификаторы посылок (через запятую)"),
            ("reception_act_id", "ID акта приемки"),
            ("store_id", "ID ЦФЗ"),
            ("delivery_id", "ID доставки"),
            ("refund_act_id", "ID акта возврата"),
            ("count_of_packages", "Количество посылок (для PICKED_UP) (default = 1)")
        ]

        for key, label_text in fields:
            label = QLabel(label_text)
            entry = QLineEdit()
            entry.textChanged.connect(self.validate)

            left_layout.addWidget(label)
            left_layout.addWidget(entry)

            self.entries[key] = entry

        # --- RIGHT SIDE ---
        right_layout = QVBoxLayout()

        buttons = [
            ButtonConfig("btn_reception", "NOT_RECEIVED -> PLACEMENT", self.copy_reception),
            ButtonConfig("btn_sorting", "PLACEMENT -> READY", self.copy_placement),
            ButtonConfig("btn_in_delivery", "PICKING -> IN_DELIVERY", self.copy_in_delivery),
            ButtonConfig("btn_delivered", "IN_DELIVERY -> DELIVERED", self.copy_delivered),
            ButtonConfig("btn_picked_up", "READY_FOR_PICKUP -> PICKED_UP", self.copy_picked_up),
            ButtonConfig("btn_return_processing", "PICKED_UP -> PROCESSING", self.copy_processing),
            ButtonConfig("btn_return_ready_for_refund", "PROCESSING -> READY_FOR_REFUND",
                         self.copy_return_ready_for_refund),
            ButtonConfig("btn_return_refunded", "READY_FOR_REFUND -> REFUNDED", self.copy_return_refunded),

        ]

        # self.btn_reception = QPushButton("NOT_RECEIVED -> PLACEMENT")
        # self.btn_reception.setEnabled(False)
        # self.btn_reception.clicked.connect(self.copy_reception)

        # self.btn_sorting = QPushButton("PLACEMENT -> READY")
        # self.btn_sorting.setEnabled(False)
        # self.btn_sorting.clicked.connect(self.copy_placement)
        #
        # self.btn_in_delivery = QPushButton("PICKING -> IN_DELIVERY")
        # self.btn_in_delivery.setEnabled(False)
        # self.btn_in_delivery.clicked.connect(self.copy_in_delivery)
        #
        # self.btn_delivered = QPushButton("IN_DELIVERY -> DELIVERED")
        # self.btn_delivered.setEnabled(False)
        # self.btn_delivered.clicked.connect(self.copy_delivered)
        #
        # self.btn_picked_up = QPushButton("PICKED_UP")
        # self.btn_picked_up.setEnabled(False)
        # self.btn_picked_up.clicked.connect(self.copy_picked_up)

        # self.btn_return_processing = QPushButton("PICKED_UP -> PROCESSING")
        # self.btn_return_processing.setEnabled(False)
        # self.btn_return_processing.clicked.connect(self.copy_processing)

        # self.btn_return_ready_for_refund = QPushButton("PROCESSING -> READY_FOR_REFUND")
        # self.btn_return_ready_for_refund.setEnabled(False)
        # self.btn_return_ready_for_refund.clicked.connect(self.copy_return_ready_for_refund)

        # self.btn_return_refunded = QPushButton("READY_FOR_REFUND -> REFUNDED")
        # self.btn_return_refunded.setEnabled(False)
        # self.btn_return_refunded.clicked.connect(self.copy_return_refunded)

        for btn in buttons:
            button = QPushButton(btn.text)
            button.setEnabled(btn.enabled)
            button.clicked.connect(btn.func)
            setattr(self, btn.name, button)
            right_layout.addWidget(button)

        # right_layout.addWidget(self.btn_reception)
        # right_layout.addWidget(self.btn_sorting)
        # right_layout.addWidget(self.btn_in_delivery)
        # right_layout.addWidget(self.btn_delivered)
        # #
        # right_layout.addWidget(self.btn_picked_up)
        # right_layout.addWidget(self.btn_return_processing)
        # right_layout.addWidget(self.btn_return_ready_for_refund)
        # right_layout.addWidget(self.btn_return_refunded)
        right_layout.addStretch()

        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

    # --- STYLE ---
    def dark_style(self):
        return """
        QWidget {
            background-color: #2b2b2b;
            color: #ffffff;
            font-size: 14px;
        }
        QLineEdit {
            background-color: #3c3f41;
            border: 1px solid #555;
            padding: 6px;
            border-radius: 6px;
        }
        QPushButton {
            background-color: #4e5254;
            border-radius: 8px;
            padding: 8px;
        }
        QPushButton:disabled {
            background-color: #2f2f2f;
            color: #777;
        }
        QPushButton:hover:!disabled {
            background-color: #6c7072;
        }
        """

    # --- HELPERS ---
    def get_packages_list(self):
        raw = self.entries["packages"].text()
        packages_list = [p.strip() for p in raw.split(",") if p.strip()]
        packages_list_normalized = [normalize_string(p) for p in packages_list]
        return packages_list_normalized

    def get_reception_act_id(self):
        raw = self.entries["reception_act_id"].text()
        return normalize_string(raw)

    def get_store_id(self):
        raw = self.entries["store_id"].text()
        return normalize_string(raw)

    def get_delivery_id(self):
        raw = self.entries["delivery_id"].text()
        return normalize_string(raw)

    def get_refund_act_id(self):
        raw = self.entries["refund_act_id"].text()
        return normalize_string(raw)

    def get_count_of_packages(self) -> int:
        raw = self.entries["count_of_packages"].text()
        if raw != "":
            try:
                return int(raw)
            except:
                QMessageBox.information(self, "Ошибка", "Проблема с количеством посылок."
                                                        " Установлено значение по умолчанию = 1")
        return 1

    def copy_to_clipboard(self, data):
        text = json.dumps(data, indent=4, ensure_ascii=False)
        QApplication.clipboard().setText(text)
        QMessageBox.information(self, "Готово", "Скопировано в буфер обмена")

    # --- Shipments ---
    def copy_reception(self):
        data = {
            "orderId": self.get_reception_act_id(),
            "receivedPackages": self.get_packages_list(),
            "refusedPackages": []
        }
        self.copy_to_clipboard(data)

    def copy_placement(self):
        data = {
            "eventId": str(uuid.uuid4()),
            "sendingTimestamp": datetime.now().isoformat(timespec='milliseconds') + "Z",
            "storeId": self.get_store_id(),
            "parcelIds": self.get_packages_list()
        }
        self.copy_to_clipboard(data)

    def copy_in_delivery(self):
        data = {
            "orderId": self.get_delivery_id(),
            "warehouseId": self.get_store_id(),
            "state": "ReadyForDelivery",
            "version": 4,
            "userId": "3575a2f8-fca7-424b-dad-56c415bbe176"
        }
        self.copy_to_clipboard(data)

    def copy_delivered(self):
        data = {
            "timestamp": datetime.now().isoformat(timespec='milliseconds') + "Z",
            "orderId": self.get_delivery_id(),
            "warehouseId": self.get_store_id(),
            "packageIdentifiers": self.get_packages_list()
        }
        self.copy_to_clipboard(data)

    # --- Возвраты ----

    def init_return_packages_barcodes(self):
        count_of_packages = self.get_count_of_packages()
        self.return_packages_array = [{
            "packageId": str(uuid.uuid4()),
            "barcode": f"SMM{random.randint(10 ** 11, 10 ** 12 - 1)}",
        } for i in range(count_of_packages)]

    def copy_picked_up(self):
        self.init_return_packages_barcodes()
        data = {
            "timestamp": datetime.now().isoformat(timespec='milliseconds') + "Z",
            "orderId": self.get_delivery_id(),
            "warehouseId": self.get_store_id(),
            "packages": self.return_packages_array
        }
        self.copy_to_clipboard(data)

    def copy_processing(self):
        if self.return_packages_array:
            data = {
                "timestamp": datetime.now().isoformat(timespec='milliseconds') + "Z",
                "orderId": self.get_reception_act_id(),
                "warehouseId": self.get_store_id(),
                "packages": self.return_packages_array
            }
            self.copy_to_clipboard(data)
        else:
            QMessageBox.information(self, "Неуспешно", "Сначала проведи сбор (PICKED_UP), "
                                                       "чтобы определить посылки")

    def copy_return_ready_for_refund(self):
        data = {
            "eventId": str(uuid.uuid4()),
            "sendingTimestamp": datetime.now().isoformat() + "000Z",
            "storeId": self.get_store_id(),
            "parcelIds": self.get_packages_list(),
        }
        self.copy_to_clipboard(data)

    def copy_return_refunded(self):
        data = {
            "orderId": self.get_refund_act_id(),
            "refundedPackages": self.get_packages_list(),
        }
        self.copy_to_clipboard(data)

    # --- VALIDATION ---

    def validate(self):
        packages = self.entries["packages"].text()
        reception = self.entries["reception_act_id"].text()
        store = self.entries["store_id"].text()
        delivery = self.entries["delivery_id"].text()

        # прямые
        self.btn_reception.setEnabled(bool(packages and reception))
        self.btn_sorting.setEnabled(bool(packages and store))
        self.btn_in_delivery.setEnabled(bool(delivery and store))
        self.btn_delivered.setEnabled(bool(packages and store and delivery))
        # возвратные
        self.btn_picked_up.setEnabled(bool(packages and store and delivery))
        self.btn_return_processing.setEnabled(bool(packages and store and delivery))
        self.btn_return_ready_for_refund.setEnabled(bool(packages and store and delivery))
        self.btn_return_refunded.setEnabled(bool(packages and store and delivery))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())

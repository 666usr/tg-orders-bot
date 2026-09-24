"""Экспорт заявок в файл Excel (xlsx)."""

from openpyxl import Workbook

import storage

HEADERS = ["№", "Дата", "Имя", "Контакт", "Задача", "Статус"]
COLUMN_WIDTHS = [6, 18, 20, 24, 40, 12]


def export_orders_to_xlsx(path, db_path=None, limit=1000):
    """Сохраняет заявки в xlsx-файл и возвращает путь к нему."""
    orders = storage.list_orders(db_path=db_path, limit=limit)

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Заявки"
    sheet.append(HEADERS)

    for order in reversed(orders):  # в хронологическом порядке
        sheet.append(
            [
                order["id"],
                order["created_at"],
                order["name"],
                order["contact"],
                order["description"],
                order["status"],
            ]
        )

    for index, width in enumerate(COLUMN_WIDTHS, start=1):
        letter = sheet.cell(row=1, column=index).column_letter
        sheet.column_dimensions[letter].width = width

    workbook.save(path)
    return path

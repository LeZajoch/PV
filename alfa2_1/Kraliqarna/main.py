# main.py
import PySimpleGUI as sg
import csv
import datetime
from models.customer import Customer
from models.product import Product
from models.order import Order
from models.db import get_db_connection

###########################################
# Funkce pro import CSV
###########################################

def import_customers_from_csv(csv_file):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        with open(csv_file, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                first_name = row['first_name']
                last_name = row['last_name']
                email = row['email']
                is_active = row['is_active'].lower() in ('true', '1')
                date_registered = row['date_registered']  # Např. "2025-01-01 10:00:00"

                cursor.execute("""
                    INSERT INTO Customers (first_name, last_name, email, is_active, date_registered)
                    VALUES (?, ?, ?, ?, ?)
                """, (first_name, last_name, email, is_active, date_registered))
            conn.commit()
        sg.Popup("Import zákazníků z CSV proběhl úspěšně.")
    except Exception as e:
        conn.rollback()
        sg.Popup(f"Nastala chyba při importu zákazníků: {e}")
    finally:
        cursor.close()
        conn.close()

def import_products_from_csv(csv_file):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        with open(csv_file, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                product_name = row['product_name']
                price = float(row['price'])
                product_status = row['product_status']
                created_at = row['created_at']  # "2025-01-01 10:00:00"

                cursor.execute("""
                    INSERT INTO Products (product_name, price, product_status, created_at)
                    VALUES (?, ?, ?, ?)
                """, (product_name, price, product_status, created_at))
            conn.commit()
        sg.Popup("Import produktů z CSV proběhl úspěšně.")
    except Exception as e:
        conn.rollback()
        sg.Popup(f"Nastala chyba při importu produktů: {e}")
    finally:
        cursor.close()
        conn.close()

###########################################
# Report
###########################################
def generate_orders_report():
    """
    Ukázka reportu: seznam objednávek + zákazník + celková cena
    (z tabulek Orders, OrderItems, Products, Customers).
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        sql = """
            SELECT
                o.order_id,
                c.first_name,
                c.last_name,
                o.order_status,
                SUM(p.price * oi.quantity) AS total_price
            FROM Orders o
                INNER JOIN Customers c ON o.customer_id = c.customer_id
                INNER JOIN OrderItems oi ON o.order_id = oi.order_id
                INNER JOIN Products p ON oi.product_id = p.product_id
            GROUP BY
                o.order_id, c.first_name, c.last_name, o.order_status
            ORDER BY o.order_id
        """
        cursor.execute(sql)
        rows = cursor.fetchall()

        report_data = "Order ID | Customer | Status | Total Price\n"
        report_data += "-" * 50 + "\n"
        for row in rows:
            order_id, first_name, last_name, order_status, total_price = row
            report_data += f"{order_id} | {first_name} {last_name} | {order_status} | {round(total_price,2)}\n"

        sg.PopupScrolled(report_data, title="Report objednávek")
    except Exception as e:
        sg.Popup(f"Chyba při generování reportu: {e}")
    finally:
        cursor.close()
        conn.close()

###########################################
# GUI - hlavní okno
###########################################
def main():
    sg.theme('SystemDefault')

    layout = [
        [sg.Text("Jednoduchá E-shop Aplikace", font=("Helvetica", 16, "bold"))],
        [sg.Button("Zobrazit zákazníky"), sg.Button("Přidat zákazníka"), sg.Button("Smazat zákazníka")],
        [sg.Button("Import Zákazníků z CSV"), sg.Button("Import Produktů z CSV")],
        [sg.Button("Vytvořit objednávku"), sg.Button("Report objednávek")],
        [sg.Exit()]
    ]

    window = sg.Window("E-shop", layout, size=(500, 250))

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Exit":
            break

        elif event == "Zobrazit zákazníky":
            customers = Customer.all()
            msg = "customer_id | jméno | email | aktivní\n"
            msg += "-"*50 + "\n"
            for c in customers:
                msg += f"{c.customer_id} | {c.first_name} {c.last_name} | {c.email} | {c.is_active}\n"
            sg.PopupScrolled(msg, title="Zákazníci")

        elif event == "Přidat zákazníka":
            layout_add = [
                [sg.Text("Jméno:"), sg.Input(key='first_name')],
                [sg.Text("Příjmení:"), sg.Input(key='last_name')],
                [sg.Text("Email:"), sg.Input(key='email')],
                [sg.Text("Aktivní (1/0):"), sg.Input(key='is_active', default_text='1')],
                [sg.Button("Uložit"), sg.Button("Storno")]
            ]
            window_add = sg.Window("Nový zákazník", layout_add)
            while True:
                ev_add, val_add = window_add.read()
                if ev_add in (sg.WIN_CLOSED, "Storno"):
                    window_add.close()
                    break
                elif ev_add == "Uložit":
                    first_name = val_add['first_name']
                    last_name = val_add['last_name']
                    email = val_add['email']
                    is_active = (val_add['is_active'] == '1')
                    new_customer = Customer(first_name=first_name, last_name=last_name, email=email, is_active=is_active)
                    new_customer.save()
                    sg.Popup("Zákazník uložen.")
                    window_add.close()
                    break

        elif event == "Smazat zákazníka":
            customer_id = sg.popup_get_text("Zadejte ID zákazníka ke smazání:")
            if customer_id:
                cust = Customer.get_by_id(int(customer_id))
                if cust:
                    cust.delete()
                    sg.Popup("Zákazník smazán.")
                else:
                    sg.Popup("Zákazník nenalezen.")

        elif event == "Import Zákazníků z CSV":
            filepath = sg.popup_get_file("Vyberte CSV soubor:", file_types=(("CSV Files", "*.csv"),))
            if filepath:
                import_customers_from_csv(filepath)

        elif event == "Import Produktů z CSV":
            filepath = sg.popup_get_file("Vyberte CSV soubor:", file_types=(("CSV Files", "*.csv"),))
            if filepath:
                import_products_from_csv(filepath)

        elif event == "Vytvořit objednávku":
            customer_id = sg.popup_get_text("Zadejte ID zákazníka (např. 1):")
            if not customer_id:
                continue
            try:
                # Ukázka vytvoření jedné objednávky s pevnými položkami (pro demonstraci).
                order = Order(customer_id=int(customer_id), order_status='pending')
                # Tady si můžeme vybrat (product_id, quantity) – v reálu by se vytvářelo přes další GUI
                order.items.append((1, 2))  # Např. product_id=1, quantity=2
                order.items.append((2, 1))
                order.save()
                sg.Popup("Objednávka vytvořena.")
            except Exception as e:
                sg.Popup(f"Chyba při vytváření objednávky: {e}")

        elif event == "Report objednávek":
            generate_orders_report()

    window.close()


if __name__ == '__main__':
    main()

import os
import time

LOCK_FILE = "lock.dat"


def main():
    try:
        # Otevřeme soubor v binárním režimu pro čtení a zápis, nebo ho vytvoříme
        with open(LOCK_FILE, "rb+") as file:
            # Přečteme první byte
            first_byte = file.read(1)

            # Kontrola zámku
            if first_byte == b'\xFF':
                print("Již běží jiná instance programu.")
                return

            # Přepíšeme první byte na b'\xFF' (zamkneme soubor)
            file.seek(0)  # Vrátíme kurzor na začátek
            file.write(b'\xFF')
            file.flush()  # Ujistíme se, že data jsou zapsána do souboru

            print("Program běží... (simuluji běh na 10 sekund)")
            time.sleep(10)  # Simulace běhu programu

            # Po skončení programu zapíšeme zpět b'\x00' (odemkneme soubor)
            file.seek(0)
            file.write(b'\x00')
            print("Program ukončen a zámek uvolněn.")

    except FileNotFoundError:
        # Pokud soubor neexistuje, vytvoříme ho a zapíšeme b'\x00'
        with open(LOCK_FILE, "wb+") as file:
            file.write(b'\x00')
        print("Vytvořen zámek. Restartujte program.")

    except Exception as e:
        print(f"Nastala chyba: {e}")


if __name__ == "__main__":
    main()

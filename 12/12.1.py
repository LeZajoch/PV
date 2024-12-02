import time
import multiprocessing

def vypis_cisel():
    for i in range(0,10):
        print(i)
        time.sleep(1)

if __name__ == "__main__":
  print("ZACATEK PROGRAMU")
  p1 = multiprocessing.Process(target=vypis_cisel)
  p1.start()
  print("KONEC PROGRAMU")



#Pozorujte co se změnilo a pokuste se odpovědět na následující otázky:
#Je v programu chyba když vypisuje KONEC PROGRAMU dříve než skončí?                     NE
#Kolik paralelních procesů bylo vlastně spuštěno? Jeden nebo dva?                       1 se spustil 2 bezeli celkem

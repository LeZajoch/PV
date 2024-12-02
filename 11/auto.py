

import unittest

from auto_test import Auto

class MotorTestCase(unittest.TestCase):

    def test_defaultni_hodnoty(self):
        motor = Motor()
        self.assertEqual(motor.get_typ_paliva(), "benzin")

    def test_typ_paliva(self):
        motor = Motor()
        motor.set_typ_paliva("nafta")
        self.assertEqual(motor.get_typ_paliva(), "nafta")
        motor.set_typ_paliva("benzin")
        self.assertEqual(motor.get_typ_paliva(), "benzin")

        with self.assertRaises(Exception):
            motor.set_typ_paliva("vodík")

        with self.assertRaises(Exception):
            motor.set_typ_paliva("baterie")

        with self.assertRaises(Exception):
            motor.set_typ_paliva(None)

        with self.assertRaises(Exception):
            motor.set_typ_paliva(123)


class AutoTestCase(unittest.TestCase):

    def test_dedicnost(self):
        """
        Test ověřuje, zda-li jsou třídy OsobniAuto a NakladniAuto potomky třídy Auto.
        """
        self.assertTrue(issubclass(OsobniAuto, Auto))
        self.assertTrue(issubclass(NakladniAuto, Auto))

    def test_osobni_auto(self):
        auto = OsobniAuto()
        self.assertEqual(auto.get_spotreba_na_100km(), 10)
        self.assertAlmostEqual(auto.get_kapacita_nadrze(), 50.0)
        self.assertAlmostEqual(auto.get_palivo(), 0.0)

        with self.assertRaises(Exception):
            auto.set_kapacita_nadrze(-1)
        with self.assertRaises(Exception):
            auto.set_kapacita_nadrze("100")
        with self.assertRaises(Exception):
            auto.set_kapacita_nadrze(Motor())

    def test_nakladni_auto(self):
        kamion = NakladniAuto()
        self.assertEqual(kamion.get_spotreba_na_100km(), 20)
        self.assertAlmostEqual(kamion.get_kapacita_nadrze(), 150.0)
        self.assertAlmostEqual(kamion.get_palivo(), 0.0)

        with self.assertRaises(Exception):
            kamion.set_kapacita_nadrze(-1)
        with self.assertRaises(Exception):
            kamion.set_kapacita_nadrze(1 - 5j)
        with self.assertRaises(Exception):
            auto.set_kapacita_nadrze(Auto())

    def test_pridani_motoru_osobni_auto(self):
        auto = OsobniAuto()
        with self.assertRaises(Exception):
            auto.get_motor()
        with self.assertRaises(Exception):
            auto.get_typ_paliva()

        motor = Motor()
        motor.set_typ_paliva("benzin")
        auto.set_motor(motor)
        self.assertEqual(auto.get_typ_paliva(), "benzin")

        with self.assertRaises(Exception):
            auto.set_motor(None)
        with self.assertRaises(Exception):
            auto.set_motor([1,2,3])
        with self.assertRaises(Exception):
            auto.set_motor("benzin")
        with self.assertRaises(Exception):
            auto.set_motor(OsobniAuto())

    def test_auto_pridani_motoru_nakladni_auto(self):
            nakladak = NakladniAuto()
            with self.assertRaises(Exception):
                nakladak.get_motor()
            with self.assertRaises(Exception):
                nakladak.get_typ_paliva()

            motor = Motor()
            motor.set_typ_paliva("nafta")
            nakladak.set_motor(motor)
            self.assertEqual(nakladak.get_typ_paliva(), "nafta")

            with self.assertRaises(Exception):
                nakladak.set_motor(None)
            with self.assertRaises(Exception):
                nakladak.set_motor([1, 2, 3])
            with self.assertRaises(Exception):
                nakladak.set_motor("benzin")
            with self.assertRaises(Exception):
                nakladak.set_motor(OsobniAuto())

    def test_takovani_osobni_auto(self):
        motor = Motor()
        motor.set_typ_paliva("benzin")

        auto = OsobniAuto()
        auto.set_kapacita_nadrze(40)
        auto.set_motor(motor)
        self.assertAlmostEqual(auto.get_palivo(), 0)

        auto.tankuj("benzin", 30.5)
        self.assertAlmostEqual(auto.get_palivo(), 30.5)

        auto2 = OsobniAuto()
        auto2.set_kapacita_nadrze(40)
        with self.assertRaises(Exception):
            auto.tankuj("benzin",40.1)
        with self.assertRaises(Exception):
            auto2.tankuj("benzin",-1)
        with self.assertRaises(Exception):
            auto2.tankuj("benzin","10")
        with self.assertRaises(Exception):
            auto2.tankuj("benzin",10 + 6j)

    def test_takovani_nakladak(self):
        motor = Motor()
        motor.set_typ_paliva("nafta")

        nakladak = NakladniAuto()
        nakladak.set_kapacita_nadrze(100)
        nakladak.set_motor(motor)
        self.assertAlmostEqual(nakladak.get_palivo(), 0)

        nakladak.tankuj("nafta", 99.5)
        self.assertAlmostEqual(nakladak.get_palivo(), 99.5)

        nakladak2 = OsobniAuto()
        nakladak2.set_kapacita_nadrze(100)
        with self.assertRaises(Exception):
            nakladak2.tankuj("benzin",40.1)
        with self.assertRaises(Exception):
            nakladak2.tankuj("nafta",-1)
        with self.assertRaises(Exception):
            nakladak2.tankuj("nafta","benzin")
        with self.assertRaises(Exception):
            nakladak2.tankuj(Motor(),10)


class JizdaTestCase(unittest.TestCase):

    def test_jizda_s_dostatkem_paliva_osobni_auto(self):
        auto = OsobniAuto()
        motor = Motor()
        auto.set_motor(motor)
        auto.tankuj("benzin",50)
        auto.jed_na_vzdalenost(100)
        self.assertAlmostEqual(auto.get_palivo(), 40)

    def test_jizda_bez_paliva_osobni_auto(self):
        auto = OsobniAuto()
        motor = Motor()
        auto.set_motor(motor)
        with self.assertRaises(Exception):
            auto.jed_na_vzdalenost(50)

    def test_jizda_s_nedostatkem_paliva_osobni_auto(self):
        auto = OsobniAuto()
        motor = Motor()
        auto.set_motor(motor)
        auto.tankuj("benzin",5)
        with self.assertRaises(Exception):
            auto.jed_na_vzdalenost(100)

    def test_jizda_s_dostatkem_paliva_nakladak(self):
        nakladak = NakladniAuto()
        motor = Motor()
        nakladak.set_motor(motor)
        nakladak.tankuj("benzin", 13.54)
        nakladak.jed_na_vzdalenost(8.43)
        self.assertGreater(nakladak.get_palivo(), 11.7)
        self.assertLess(nakladak.get_palivo(), 11.9)

    def test_jizda_bez_paliva(self):
        nakladak = NakladniAuto()
        motor = Motor()
        nakladak.set_motor(motor)
        with self.assertRaises(Exception):
            nakladak.jed_na_vzdalenost(0.5)

    def test_jizda_nevalidni_vstup(self):
        nakladak = NakladniAuto()
        motor = Motor()
        nakladak.set_motor(motor)
        nakladak.tankuj("benzin",50)
        with self.assertRaises(Exception):
            nakladak.jed_na_vzdalenost(-1)
        with self.assertRaises(Exception):
            nakladak.jed_na_vzdalenost(None)



if __name__ == '__main__':
    unittest.main()
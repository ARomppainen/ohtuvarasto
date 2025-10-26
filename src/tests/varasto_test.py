import unittest
from varasto import Varasto


class TestVarasto(unittest.TestCase):
    def setUp(self):
        self.varasto = Varasto(10)

    def test_konstruktori_luo_tyhjan_varaston(self):
        # https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertAlmostEqual
        self.assertAlmostEqual(self.varasto.saldo, 0)

    def test_uudella_varastolla_oikea_tilavuus(self):
        self.assertAlmostEqual(self.varasto.tilavuus, 1)

    def test_uudella_varastolla_tilavuus_nolla_jos_arvo_negatiivinen(self):
        self.assertAlmostEqual(Varasto(-1).tilavuus, 0)

    def test_uudella_varastolla_alkusaldo_nolla_jos_arvo_negatiivinen(self):
        self.assertAlmostEqual(Varasto(10, -1).saldo, 0)

    def test_uudella_varastolla_alkusaldo_ei_voi_ylittaa_tilavuutta(self):
        self.assertAlmostEqual(Varasto(10, 11).saldo, 10)

    def test_lisays_lisaa_saldoa(self):
        self.varasto.lisaa_varastoon(8)

        self.assertAlmostEqual(self.varasto.saldo, 8)

    def test_lisays_ei_tee_mitaan_jos_arvo_negatiivinen(self):
        self.varasto.lisaa_varastoon(-1)
        self.assertAlmostEqual(self.varasto.saldo, 0)
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 10)

    def test_lisays_ei_voi_ylittaa_tilavuutta(self):
        self.varasto.lisaa_varastoon(11)
        self.assertAlmostEqual(self.varasto.saldo, 10)
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 0)

    def test_lisays_lisaa_pienentaa_vapaata_tilaa(self):
        self.varasto.lisaa_varastoon(8)

        # vapaata tilaa pitäisi vielä olla tilavuus-lisättävä määrä eli 2
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 2)

    def test_ottaminen_palauttaa_oikean_maaran(self):
        self.varasto.lisaa_varastoon(8)

        saatu_maara = self.varasto.ota_varastosta(2)

        self.assertAlmostEqual(saatu_maara, 2)

    def test_ottaminen_lisaa_tilaa(self):
        self.varasto.lisaa_varastoon(8)

        self.varasto.ota_varastosta(2)

        # varastossa pitäisi olla tilaa 10 - 8 + 2 eli 4
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 4)

    def test_ottaminen_ei_muuta_tilaa_negatiivisilla_arvoilla_ja_palauttaa_nollan(self):
        self.varasto.lisaa_varastoon(3)
        self.assertAlmostEqual(self.varasto.ota_varastosta(-1), 0)
        self.assertAlmostEqual(self.varasto.saldo, 3)
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 7)

    def test_ottaminen_palauttaa_koko_saldon_jos_maara_ylittaa_sen(self):
        self.varasto.lisaa_varastoon(3)
        self.assertAlmostEqual(self.varasto.ota_varastosta(4), 3)
        self.assertAlmostEqual(self.varasto.saldo, 0)
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 10)

    def test_varaston_tila_voidaan_tulostaa(self):
        self.varasto.lisaa_varastoon(3)
        self.assertEqual(str(self.varasto), "saldo = 3, vielä tilaa 7")

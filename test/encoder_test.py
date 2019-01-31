import unittest
from mock.encoder import Encoder

class EncoderTest(unittest.TestCase):
    def test(self):
            encoder = Encoder("E")
            encoder.listen_until(5)
            self.assertEqual(encoder.current_step,5)

            encoder.listen_until(3)
            self.assertEqual(encoder.current_step,3)

            encoder = Encoder("W")
            encoder.listen_until(15)
            self.assertEqual(encoder.current_step,15)

            encoder.listen_until(-5)
            self.assertEqual(encoder.current_step,0)

            encoder.listen_until(150)
            self.assertEqual(encoder.current_step,120)

if __name__ == '__main__':
    unittest.main()

from .form import BarcodeForm
from .reader import InputDeviceReader


class BarcodeScanner(object):

    def __init__(self, device):
        self.reader = InputDeviceReader(device)
        self.reader.start()

    def __del__(self):

        try:
            reader = getattr(self, 'reader')
        except AttributeError:
            pass
        else:
            reader.join()

    def scan_code(self, gui=True):
        code = None

        if gui:
            form = BarcodeForm(self.reader)
            form.mainloop()
            code = form.code
        else:

            while True:
                input('Please scan a BARCODE, then press ENTER...')

                code = self.reader.read()

                print('Please confirm the input "{}"'.format(code))
                ans = input('Enter [y]es, (r)epeat, or value: ')
                ans = ans.lower()

                if not ans or ans == 'y':
                    break
                elif ans == 'r':
                    continue
                else:
                    code = ans
                    break

        return code


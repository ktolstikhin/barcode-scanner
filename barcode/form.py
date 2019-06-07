import tkinter as tk


class BarcodeForm(tk.Tk):

    UPDATE_DELAY = 1000

    def __init__(self, reader):
        super().__init__()
        self.title('Scan or enter a barcode value.')

        tk.Label(self, text='Barcode').grid(
            row=0, column=0, padx=5)

        self.code_entry = tk.StringVar(self, value='')
        entry = tk.Entry(self, width=50, textvariable=self.code_entry)
        entry.bind('<Return>', func=lambda _: self.submit())
        entry.grid(
            row=0, column=1, padx=5)

        tk.Button(self, text='OK', command=self.submit).grid(
            row=0, column=2, padx=5)

        self.protocol('WM_DELETE_WINDOW', self.close_form)

        self.code = ''
        self.reader = reader
        self.update_entry()

    def update_entry(self):
        code = self.reader.read()

        if code:
            self.code_entry.set(code)

        self.after_id = self.after(self.UPDATE_DELAY, self.update_entry)

    def submit(self):
        self.code = self.code_entry.get()

        if not self.code:
            return

        self.close_form()

    def close_form(self):
        self.after_cancel(self.after_id)
        self.destroy()


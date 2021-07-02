from time import sleep

from guizero import App, TextBox

class MeasureTerminal:
    textBox = None

    @classmethod
    def print(cls, str):
        tb = MeasureTerminal.textBox
        if tb != None:
            tb.append(str)
            tb.tk.see('end')


    def display(self):
        sleep(15)
        app = App(layout="auto")

        textBox = TextBox(
            app,
            multiline=True,
            width="fill",
            height="fill",
            text="",
            enabled=False,
            scrollbar=True
        )
        MeasureTerminal.textBox = textBox
        textBox.font = "arial"
        app.full_screen = True
        app.display()

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
        MeasureTerminal = textBox
        # change fonts to be one you like
        textBox.font = "arial"
        # ml_textbox.append("12345")
        # ml_textbox.append("12345")
        # ml_textbox.append("12345")
        # ml_textbox.append("12345")
        # ml_textbox.append("12345")
        # ml_textbox.append("12345")
        # ml_textbox.append("12345")
        # ml_textbox.tk.see('end')
        #
        # ml_textbox.append("125")
        # ml_textbox.append("124")
        # ml_textbox.tk.see('end')

        app.full_screen = True
        app.display()

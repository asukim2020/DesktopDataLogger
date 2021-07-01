
# class FileUtil:



# Test Code
if __name__ == "__main__":
    from guizero import App, TextBox

    app = App(layout="auto")

    ml_textbox = TextBox(
        app,
        multiline=True,
        width="fill",
        height="fill",
        text="multiline\ntext box",
        enabled=False,
        scrollbar=True
    )

    # change fonts to be one you like
    ml_textbox.font = "arial"
    ml_textbox.append("12345")
    ml_textbox.append("12345")
    ml_textbox.append("12345")
    ml_textbox.append("12345")
    ml_textbox.append("12345")
    ml_textbox.append("12345")
    ml_textbox.append("12345")
    ml_textbox.tk.see('end')

    ml_textbox.append("125")
    ml_textbox.append("124")
    ml_textbox.tk.see('end')

    app.full_screen = True
    app.display()

    # f = open("test.csv", 'w')
    # f.write("1234\n")
    # f.write("1234\n")
    # f.write("1234\n")
    #
    # f.close()
    #
    # rf = open("test.csv", 'r')
    # while True:
    #     line = rf.readline()
    #     if not line: break
    #     print(line, end='')
    # rf.close()
    #
    # f = open("test.csv", 'w')
    # f.write("123456\n")
    # f.write("123456\n")
    # f.write("123456\n")
    #
    # f.close()

    # rf = open("1234.csv", 'r')
    # while True:
    #     line = rf.readline()
    #     if not line: break
    #     print(line, end='')
    # rf.close()




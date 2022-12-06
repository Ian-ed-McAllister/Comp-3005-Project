import tkinter as tk
from tkinter import ttk
import middleware


LARGEFONT = ("Verdana", 35)


class tkinterApp(tk.Tk):

    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):

        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        # creating a container
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=3)
        container.grid_columnconfigure(0, weight=1)

        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (StartPage, Page1, Page2):

            frame = F(container, self)

            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

# first window frame startpage


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # label of frame Layout 2
        label = ttk.Label(self, text="Main Page")

        # putting the grid in its place by using
        # grid
        label.grid(row=0, column=4, padx=10, pady=10)

        book_box = ttk.Treeview(self, columns=(
            'title', 'isbn', 'pages', 'price'), show='headings')

        book_box.heading("title", text="title")

        book_box.heading("isbn", text="isbn")

        book_box.heading("pages", text="pages")
        book_box.heading("price", text="price")

        book_box.grid(row=1, column=1, padx=10, pady=10)
        scrollbar = ttk.Scrollbar(
            book_box, orient=tk.VERTICAL, command=book_box.yview)
        scrollbar2 = ttk.Scrollbar(
            book_box, orient=tk.HORIZONTAL, command=book_box.xview)

        book_box.configure(yscrollcommand=scrollbar.set,
                           xscrollcommand=scrollbar2)

        middleware.get_books()
        for book in middleware.get_books():

            book_box.insert("", 'end', values=(
                book['title'], book['isbn'], book['numpages'], book['price']))

        # TODO: ADD TO CART SOMEHOW, SEARCH

        # button1 = ttk.Button(self, text="Page 1",
        #                      command=lambda: controller.show_frame(Page1))

        # putting the button in its place by
        # using grid
        # button1.grid(row=1, column=1, padx=10, pady=10)


# second window +frame used for login
class Page1(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Page 1", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        # button to show frame 2 with text
        # layout2
        button1 = ttk.Button(self, text="StartPage",
                             command=lambda: controller.show_frame(StartPage))

        # putting the button in its place
        # by using grid
        button1.grid(row=1, column=1, padx=10, pady=10)

        # button to show frame 2 with text
        # layout2
        button2 = ttk.Button(self, text="Page 2",
                             command=lambda: controller.show_frame(Page2))

        # putting the button in its place by
        # using grid
        button2.grid(row=2, column=1, padx=10, pady=10)


# third window frame used to checkout
class Page2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Page 2", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        # button to show frame 2 with text
        # layout2
        button1 = ttk.Button(self, text="Page 1",
                             command=lambda: controller.show_frame(Page1))

        # putting the button in its place by
        # using grid
        button1.grid(row=1, column=1, padx=10, pady=10)

        # button to show frame 3 with text
        # layout3
        button2 = ttk.Button(self, text="Startpage",
                             command=lambda: controller.show_frame(StartPage))

        # putting the button in its place by
        # using grid
        button2.grid(row=2, column=1, padx=10, pady=10)


# Driver Code
app = tkinterApp()
app.resizable(False, False)
app.title("Look Inna Book store")
app.geometry('1280x720+50+50')
app.mainloop()

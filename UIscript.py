import tkinter as tk
from tkinter import ttk
import middleware
import re

LARGEFONT = ("Verdana", 35)
#cart = []

# make it so it fist takes you to the log in from there you it will route you to either the admin side or the user side.


class tkinterApp(tk.Tk):
    # __init__ function for class tkinterApp

    def __init__(self, *args, **kwargs):

        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        # creating a container

        # IMPORTANT AFTER LOGIN SET THIS USER SO IT KNOWS WHERE TO GO AND GET THE INFO THAT IS WITHIN THE USER
        self.user = None
        print(self.user)
        # use this cart as the store the items that were added to the cart
        self.books, self.genres, self.authors = middleware.get_books()
        self.cart = []
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)
        container.columnconfigure(2, weight=1)
        container.columnconfigure(3, weight=1)
        container.columnconfigure(4, weight=1)
        container.columnconfigure(5, weight=1)

        # initializing frames to an empty array
        self.frames = {}
        self.login_frame = login_page(container, self)
        self.login_frame.grid(row=0, column=0, sticky="nsew")
        # iterating through a tuple consisting
        # of the different page layouts
        for F in (StartPage, cart_page, ):

            frame = F(container, self)

            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_login()

    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        self.refresh_vars()
        frame = self.frames[cont]
        frame.my_refresh(self)
        frame.tkraise()

    def show_login(self):
        print("IN")
        self.login_frame.tkraise()

    def show_admin(self):
        print("SHOULD SHOW ADMIN TERMINAL")

    def refresh_vars(self):
        self.books, self.genres, self.authors = middleware.get_books()


# first window frame startpage


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # BOX THAT SHOWS THE BOOKS IN THE FRAME

        self.book_box = ttk.Treeview(self, columns=(
            'id', 'title', 'isbn', "authors", 'pages', "geners", 'price', 'quantity'), show='headings')
        self.book_box.heading("id", text="id")
        self.book_box.column('id', width=0, minwidth=0)

        self.book_box.heading("title", text="title")
        self.book_box.heading("isbn", text="isbn")
        self.book_box.heading("authors", text="author(s)")
        self.book_box.heading("pages", text="pages")
        self.book_box.heading("price", text="price")
        self.book_box.heading("geners", text="geners")
        self.book_box.heading("quantity", text="quantity")
        self.book_box.grid(column=0, columnspan=7, row=0, rowspan=2)

        search_label = tk.Label(self, text="Search")
        search_label.grid(row=0, column=8)

        filler = tk.Label(self).grid(row=1, column=8)
        title_search = tk.Label(self, text="Title").grid(row=2, column=8)
        self.title_search_entry = tk.Entry(self)
        self.title_search_entry.grid(column=9, row=2)

        genre_search = tk.Label(
            self, text="genre").grid(row=3, column=8)
        self.genre_search_entry = tk.Entry(self)
        self.genre_search_entry.grid(column=9, row=3)

        isbn_search = tk.Label(self, text="ISBN").grid(row=4, column=8)
        self.isbn_search_entry = tk.Entry(self)
        self.isbn_search_entry.grid(column=9, row=4)

        author_search = tk.Label(self, text="author").grid(row=5, column=8)
        self.author_search_entry = tk.Entry(self)
        self.author_search_entry.grid(column=9, row=5)

        pages_search = tk.Label(self, text="pages").grid(row=6, column=8)
        self.pages_search_entry = tk.Entry(self)
        self.pages_search_entry.grid(column=9, row=6)

        search_button = tk.Button(
            self, text="Look up", command=lambda: self.search(controller))
        search_button.grid(row=7, column=9)

        self.title_display = tk.Label(self)
        self.title_display.grid(row=2, column=0)

        self.authors_display = tk.Label(self)
        self.authors_display.grid(row=2, column=1)

        self.genre_display = tk.Label(self)
        self.genre_display.grid(row=2, column=2)

        self.isbn_display = tk.Label(self)
        self.isbn_display.grid(row=2, column=3)

        author_display = tk.Label(self)
        author_display.grid(row=2, column=4)

        quantity_label = tk.Label(
            self, text="Quantity to purchase:").grid(row=3, column=0)
        self.number_of_books = tk.Entry(self)
        self.number_of_books.grid(row=3, column=1)

        self.error_box = tk.Label(self)
        self.error_box.grid(row=3, column=3)

        search_button = tk.Button(
            self, text="add to checkout", command=lambda: self.add_to_cart(controller))
        search_button.grid(row=3, column=2)
        self.book_box.bind('<ButtonRelease-1>', self.display_selected_item)

        self.set_books(controller.books, controller.genres, controller.authors)

        to_cart_button = ttk.Button(self, text="go to check out",
                                    command=lambda: controller.show_frame(cart_page))
        to_cart_button.grid(row=4, column=0)
        # self.search()

    def search(self, controller):
        if (len(self.title_search_entry.get()) == 0) and (len(self.genre_search_entry.get()) == 0) and ((len(self.author_search_entry.get())) == 0) and (len(self.isbn_search_entry.get()) == 0) and (len(self.pages_search_entry.get()) == 0):
            self.set_books(controller.books, controller.genres,
                           controller.authors)
        else:

            # could also be done with SQL commands ex Select * in books where title = 'harry potter'.
            search_books = controller.books.copy()
            search_genres = controller.genres.copy()
            search_authors = controller.authors.copy()
            if len(self.title_search_entry.get()) != 0:
                to_remove = []
                index = 0
                for book in search_books:
                    if self.title_search_entry.get().upper() not in book["title"].upper():
                        for genre in search_genres:
                            if genre['bid'] == book['bid']:

                                search_genres.remove(genre)
                        to_remove.append(index)

                    index += 1
                for i in reversed(to_remove):
                    search_books.remove(search_books[i])

            if len(self.genre_search_entry.get()) != 0:
                temp_index = search_genres[0]["bid"]
                remove = True
                for genre in search_genres:

                    if (temp_index != genre["bid"]):
                        if remove:
                            for book in search_books:
                                if book["bid"] == temp_index:
                                    search_books.remove(book)
                                    break
                        remove = True
                        temp_index = genre["bid"]
                    print(genre["genre"])
                    if (re.search(self.genre_search_entry.get(), genre["genre"], re.IGNORECASE)):
                        print("in")
                        remove = False
                if remove:
                    for book in search_books:
                        if book["bid"] == temp_index:
                            search_books.remove(book)
                            break

            if len(self.author_search_entry.get()) != 0:
                temp_index = search_authors[0]["bid"]
                remove = True
                for author in search_authors:

                    if (temp_index != author["bid"]):
                        if remove:
                            for book in search_books:
                                if book["bid"] == temp_index:
                                    search_books.remove(book)
                                    break
                        remove = True
                        temp_index = author["bid"]

                    if (re.search(self.author_search_entry.get(), author["authname"], re.IGNORECASE)):
                        remove = False
                if remove:
                    for book in search_books:
                        if book["bid"] == temp_index:
                            search_books.remove(book)
                            break

            if len(self.isbn_search_entry.get()) != 0:
                to_remove = []
                index = 0
                for book in search_books:
                    if self.isbn_search_entry.get() != book["isbn"]:
                        to_remove.append(index)

                    index += 1
                for index in reversed(to_remove):
                    search_books.remove(search_books[index])

            if len(self.pages_search_entry.get()) != 0 and self.pages_search_entry.get().isdigit():
                max_pages = int(self.pages_search_entry.get())
                to_remove = []
                index = 0
                for book in search_books:
                    if max_pages < int(book["numpages"]):
                        to_remove.append(index)

                    index += 1
                for index in reversed(to_remove):
                    search_books.remove(search_books[index])

            self.set_books(search_books, search_genres, search_authors)

    def set_books(self, book_list, genre_list, author_list):

        for item in self.book_box.get_children():
            self.book_box.delete(item)

        for new_book in book_list:
            if new_book["show"]:
                string = ""
                auth_string = ""
                for genre in genre_list:
                    if genre["bid"] == new_book['bid']:
                        string += genre["genre"] + " "

                for author in author_list:
                    if (author["bid"] == new_book["bid"]):
                        auth_string += author["authname"] + " "

                self.book_box.insert("", 'end', values=(
                    new_book['bid'], new_book['title'], new_book['isbn'], auth_string, new_book['numpages'], string, new_book['price'], new_book["quantity"]))

    def add_to_cart(self, controller):
        if self.book_box.selection() == ():
            self.error_box.config(text="please select a book")
            return

        try:
            val = int(self.number_of_books.get())
            selected_item = self.book_box.selection()[0]
            if (0 < val <= int(self.book_box.item(selected_item)['values'][7])):

                index = 0
                for item in controller.cart:
                    print(item)
                    if item[0] == self.book_box.item(selected_item)['values'][0]:
                        if (item[1]+val) > int(self.book_box.item(selected_item)['values'][7]):
                            self.error_box.config(
                                text="You have added too many of that item!")
                            return

                        item = (item[0], item[1]+val)

                        controller.cart[index] = item
                        self.error_box.config(text="Updated amount in cart")
                        print(controller.cart)
                        return
                    index += 1
                controller.cart.append(
                    (self.book_box.item(selected_item)['values'][0], val))
                self.error_box.config(text="Added to cart")

            else:
                self.error_box.config(
                    text="Number entered exceedes quantity in stock or is 0")
            print(controller.cart)

        except ValueError:
            self.error_box.config(
                text="please enter a number")

    def display_selected_item(self, a):
        try:
            selected_item = self.book_box.selection()[0]

            self.title_display.config(text=self.book_box.item(
                selected_item)['values'][1])
            self.authors_display.config(text=self.book_box.item(
                selected_item)['values'][3])
            self.isbn_display.config(text=self.book_box.item(
                selected_item)['values'][2])
            self.genre_display.config(text=self.book_box.item(
                selected_item)['values'][5])
        except:
            print("did not click on a valid index")

    def my_refresh(self, controller):
        self.set_books(controller.books, controller.genres,
                       controller.authors)


class cart_page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # WHAT IS NEEDED:
        # TREE VIEW FOR ITEMS IN CART
        # PLACE TO ADD SHIPPING INFO OR SELECT SAVED INFO IF APPLICABLE (NOT NULL)
        # ADD BUTTTONS TO NAVIGATE BETWEEN THE PAGES

        # button to show frame 2 with text
        # layout2
        button1 = ttk.Button(self, text="Back to Items",
                             command=lambda: controller.show_frame(StartPage))

        # putting the button in its place
        # by using grid
        button1.grid(row=0, column=8)

        self.cart_box = ttk.Treeview(self, columns=(
            "id", "title", "unit_price", "quantity", "total_price"), show='headings')
        self.cart_box.heading("id", text="id")
        self.cart_box.column('id', width=0, minwidth=0)

        self.cart_box.heading("title", text="title")
        self.cart_box.heading("unit_price", text="Unit Price")
        self.cart_box.heading("quantity", text="Quantity in cart")
        self.cart_box.heading("total_price", text="Total Price")

        self.cart_box.grid(column=0, columnspan=7, row=0, rowspan=2)

        remove_item_button = ttk.Button(
            self, text="remove selected", command=lambda: self.remove_from_cart(controller))
        remove_item_button.grid(row=3, column=0)

        # add check box to use users svaed info if it exsists
        self.my_var = tk.IntVar(self)
        self.use_saved = tk.Checkbutton(
            self, text="Use Saved", variable=self.my_var)
        self.use_saved.grid(column=8, row=2)
        self.user_card_num_label = tk.Label(
            self, text="Card Number: ").grid(column=8, row=3)
        self.user_card_num_entry = tk.Entry(self)
        self.user_card_num_entry.grid(column=9, row=3)

        self.user_card_ccv_label = tk.Label(
            self, text="CCV: ").grid(column=10, row=3)
        self.user_card_ccv_entry = tk.Entry(self)
        self.user_card_ccv_entry.grid(column=11, row=3)

        self.user_card_exp_label = tk.Label(
            self, text="expiry date (MM/YY)").grid(column=12, row=3)
        self.user_card_exp_entry = tk.Entry(self)
        self.user_card_exp_entry.grid(column=13, row=3)

        self.user_country_label = tk.Label(
            self, text="Country: ").grid(column=14, row=3)
        self.user_country_entry = tk.Entry(self)
        self.user_country_entry.grid(column=15, row=3)

        self.user_province_label = tk.Label(
            self, text="Province: ").grid(column=8, row=4)
        self.user_province_entry = tk.Entry(self)
        self.user_province_entry.grid(column=9, row=4)

        self.user_city_label = tk.Label(
            self, text="City: ").grid(column=10, row=4)
        self.user_city_entry = tk.Entry(self)
        self.user_city_entry.grid(column=11, row=4)

        self.purchase_button = tk.Button(
            self, text="Purchase Cart", command=lambda: self.make_purchase(controller))

        self.user_adress_label = tk.Label(
            self, text="Address: ").grid(column=12, row=4)
        self.user_adress_entry = tk.Entry(self)
        self.user_adress_entry.grid(column=13, row=4)

        self.user_postal_label = tk.Label(
            self, text="Postal Code: ").grid(column=14, row=4)
        self.user_postal_entry = tk.Entry(self)
        self.user_postal_entry.grid(column=15, row=4)

        purchase_button = ttk.Button(
            self, text="PURCHASE ITEMS", command=lambda: self.make_purchase(controller))
        purchase_button.grid(row=3, column=1)

        self.error_box = tk.Label(self, text="")
        self.error_box.grid(row=4, column=0)

    def my_refresh(self, controller):
        # use this fucntion to add all of the items in the cart to the tree view that will be made to store the items,
        for child in self.cart_box.get_children():
            self.cart_box.delete(child)

        print(controller.cart)
        for item in controller.cart:
            print(item[0])
            full_item_info = controller.books[item[0]-1]
            self.cart_box.insert("", "end", values=(
                full_item_info['bid'], full_item_info['title'], full_item_info['price'], item[1], float(full_item_info['price'])*item[1]))

    def remove_from_cart(self, controller):
        to_remove = self.cart_box.selection()[0]
        if to_remove == ():
            print("please select a book in the cart")
            return
        book_id = int(self.cart_box.item(to_remove)['values'][0])

        for item in controller.cart:
            if item[0] == book_id:
                controller.cart.remove(item)
                break
        self.my_refresh(controller)
        # third window frame used to checkout

    def make_purchase(self, controller):

        if self.my_var.get():
            try:
                middleware.make_order(controller.user['uid'], controller.user['cardNum'], controller.user['ccv'], controller.user['expDate'], controller.user['country'],
                                      controller.user['province'], controller.user['city'], controller.user['streetAdress'], controller.user['postalCode'], controller.cart)

                controller.cart = []
                self.my_refresh(controller)
                controller.refresh_vars()
            # if controller.user['cardNum'] ==| controller.user['ccv'] == None | controller.user['expDate'] == None | controller.user['country'] == None | controller.user['province'] == None | controller.user['streetAdresss'] == None | controller.user['city'] == None | controller.user['postalCode'] == None:
            #     self.error_box.config(
            #         text="Your User Does not have the needed saved info please enter the info properly and uncheck the box")
            #     return
            except:
                self.error_box.config(
                    text="Your User Does not have the needed saved info please enter the info properly and uncheck the box")
                return

        else:
            if (len(self.user_card_num_entry.get()) != 0 and len(self.user_card_ccv_entry.get()) != 0 and len(self.user_card_exp_entry.get()) != 0 and len(self.user_country_entry.get()) != 0 and len(self.user_province_entry.get()) != 0 and len(self.user_city_entry.get()) != 0 and len(self.user_adress_entry.get()) != 0 and len(self.user_postal_entry.get()) != 0):
                # check to see if the use saved data is checked, if not do:
                middleware.make_order(controller.user['uid'], self.user_card_num_entry.get(), self.user_card_ccv_entry.get(), self.user_card_exp_entry.get(), self.user_country_entry.get(
                ), self.user_province_entry.get(), self.user_city_entry.get(), self.user_adress_entry.get(), self.user_postal_entry.get(), controller.cart)

                controller.cart = []
                self.my_refresh(controller)
                controller.refresh_vars()


class login_page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        login_label = tk.Label(self, text="Login").grid(column=0, row=0)
        username_label = tk.Label(
            self, text="Username: ").grid(column=0, row=1)
        self.username_entry = tk.Entry(self)
        self.username_entry.grid(column=1, row=1)
        password_label = tk.Label(
            self, text="password: ").grid(column=0, row=2)
        self.password_entry = tk.Entry(self)
        self.password_entry.grid(column=1, row=2)

        login_button = tk.Button(
            self, text="Log In", command=lambda: self.check_info(controller))
        login_button.grid(column=1, row=3)

    def check_info(self, controller):
        if (len(self.username_entry.get()) != 0) and (len(self.password_entry.get()) != 0):
            controller.user = middleware.login_check(
                self.username_entry.get(), self.password_entry.get())
            if (controller.user != None):
                print(controller.user)
                if controller.user['type'] == 'A':
                    print("IN ADMIN")
                    controller.show_admin()
                else:
                    print("in other")
                    controller.show_frame(StartPage)
            print("OUT")


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
#app.resizable(False, False)
app.title("Look Inna Book store")
# app.geometry('1280x720+50+50')
app.mainloop()

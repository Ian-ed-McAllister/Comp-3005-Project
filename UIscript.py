import tkinter as tk
from tkinter import ttk
import middleware
import re

LARGEFONT = ("Verdana", 35)


class tkinterApp(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        self.user = None

        self.books, self.genres, self.authors = middleware.get_books()
        self.cart = []
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        # initializing frames to an empty dict
        self.frames = {}
        self.login_frame = login_page(container, self)
        self.login_frame.grid(row=0, column=0, sticky="nsew")
        self.register_frame = register_page(container, self)
        self.register_frame.grid(row=0, column=0, sticky="nsew")
        self.admin_frame = admin_page(container, self)
        self.admin_frame.grid(row=0, column=0, sticky="nsew")
        # iterating through a tuple consisting
        # of the different page layouts
        for F in (StartPage, cart_page, customer_info):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_login()

    # to display diffrent frames
    def show_frame(self, cont):
        self.refresh_vars()
        frame = self.frames[cont]
        frame.my_refresh(self)
        frame.tkraise()

    # to show the login page as it should not be called otherwise
    def show_login(self):

        self.login_frame.tkraise()

    # to show the register page as it should not be called otherwise
    def show_register(self):
        self.register_frame.tkraise()

    # to show admin side as it should onyl be seen by a admin user
    def show_admin(self):
        self.admin_frame.tkraise()

    # used to get current inforamtion after an update,
    def refresh_vars(self):
        self.books, self.genres, self.authors = middleware.get_books()


# This page is the main shopping page that should allow the user to put books into the cart, search books, and navigate to the other pages in the user side
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

        # entries for use in the search function
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

        # Button to run the search function
        search_button = tk.Button(
            self, text="Look up", command=lambda: self.search(controller))
        search_button.grid(row=7, column=9)

        # labels that will show information about the books when one is clicked
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

        # used for entring the number of books you would like to purchase
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

        # used to fill the book box
        self.set_books(controller.books, controller.genres, controller.authors)

        to_cart_button = ttk.Button(self, text="go to check out",
                                    command=lambda: controller.show_frame(cart_page))
        to_cart_button.grid(row=4, column=0)

        user_info_button = tk.Button(self, text="User/Shipping Info",
                                     command=lambda: controller.show_frame(customer_info))

        user_info_button.grid(row=4, column=1)

    # allows for the user to search the books, this isnt done with sql as i already have all the books stored locally so there is no need to make another query
    # It could be done by doing SELECT * FROM books WHERE title = 'harry potter' ...
    # the WHERE string could be dynamically made here and used
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

                    if (re.search(self.genre_search_entry.get(), genre["genre"], re.IGNORECASE)):

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

    # Sets the books after a search
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

    # function to add the book to the cart

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

                    if item[0] == self.book_box.item(selected_item)['values'][0]:
                        if (item[1]+val) > int(self.book_box.item(selected_item)['values'][7]):
                            self.error_box.config(
                                text="You have added too many of that item!")
                            return

                        item = (item[0], item[1]+val)

                        controller.cart[index] = item
                        self.error_box.config(text="Updated amount in cart")

                        return
                    index += 1
                controller.cart.append(
                    (self.book_box.item(selected_item)['values'][0], val))
                self.error_box.config(text="Added to cart")

            else:
                self.error_box.config(
                    text="Number entered exceedes quantity in stock or is 0")

        except ValueError:
            self.error_box.config(
                text="please enter a number")

    # used to show more information on the iten when it is clicked
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

    # used to refresh the frame after an update to the books table
    def my_refresh(self, controller):
        self.set_books(controller.books, controller.genres,
                       controller.authors)

# class that takes care of the final purchasing of items


class cart_page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        button1 = tk.Button(self, text="Back to Shopping",
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

        remove_item_button = tk.Button(
            self, text="remove selected", command=lambda: self.remove_from_cart(controller))
        remove_item_button.grid(row=3, column=0)

        # Used to either use the information in the entry boxes below or in the information saved in the database
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

        self.user_adress_label = tk.Label(
            self, text="Address: ").grid(column=12, row=4)
        self.user_adress_entry = tk.Entry(self)
        self.user_adress_entry.grid(column=13, row=4)

        self.user_postal_label = tk.Label(
            self, text="Postal Code: ").grid(column=14, row=4)
        self.user_postal_entry = tk.Entry(self)
        self.user_postal_entry.grid(column=15, row=4)

        purchase_button = tk.Button(
            self, text="PURCHASE ITEMS", command=lambda: self.make_purchase(controller))
        purchase_button.grid(row=3, column=1)

        self.error_box = tk.Label(self, text="")
        self.error_box.grid(row=4, column=0)

    def my_refresh(self, controller):
        # use this fucntion to add all of the items in the cart to the tree view that will be made to store the items,
        for child in self.cart_box.get_children():
            self.cart_box.delete(child)

        for item in controller.cart:

            full_item_info = controller.books[item[0]-1]
            self.cart_box.insert("", "end", values=(
                full_item_info['bid'], full_item_info['title'], full_item_info['price'], item[1], float(full_item_info['price'])*item[1]))

    # used to remove the item from the cart

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

    # used to purchase the items in the cart
    # calls the middleware function that will make the purchase will the refresh the information that is local
    def make_purchase(self, controller):

        if self.my_var.get():

            try:
                # calls the middleware function
                middleware.make_order(controller.user['uid'], controller.user['cardnum'], controller.user['ccv'], controller.user['expdate'], controller.user['country'],
                                      controller.user['province'], controller.user['city'], controller.user['streetaddress'], controller.user['postalcode'], controller.cart)
                # refreshed the saved data
                controller.cart = []
                self.my_refresh(controller)
                controller.refresh_vars()
                self.error_box.config(
                    text="Purchase complete")
            except Exception as error:
                print(error)
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
                self.error_box.config(
                    text="Purchase complete")


# page to deal with the login informaion
# The username and password are case sensitve
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

        register_button = tk.Button(
            self, text="Register", command=lambda: controller.show_register())
        register_button.grid(column=0, row=3)

    # calls the middleware function that will return the users information if the user exists
    def check_info(self, controller):
        if (len(self.username_entry.get()) != 0) and (len(self.password_entry.get()) != 0):
            controller.user = middleware.login_check(
                self.username_entry.get(), self.password_entry.get())
            if (controller.user != None):

                if controller.user['type'] == 'A':

                    controller.show_admin()
                else:

                    controller.show_frame(StartPage)

# page used to deal with checking the users orders and chaging the saved information


class customer_info(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # button to show frame 2 with text
        # layout2
        self.orders_box = ttk.Treeview(self, columns=(
            "oid", "from", "current", "destination"), show='headings')

        self.orders_box.heading("oid", text="Order Id")
        self.orders_box.heading("from", text="Shipped From")
        self.orders_box.heading("current", text="Current Stage")
        self.orders_box.heading("destination", text="Destination Postal Code")

        self.orders_box.grid(column=0, row=0)
        # used to get the information to change
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

        self.user_adress_label = tk.Label(
            self, text="Address: ").grid(column=12, row=4)
        self.user_adress_entry = tk.Entry(self)
        self.user_adress_entry.grid(column=13, row=4)

        self.user_postal_label = tk.Label(
            self, text="Postal Code: ").grid(column=14, row=4)
        self.user_postal_entry = tk.Entry(self)
        self.user_postal_entry.grid(column=15, row=4)

        button2 = tk.Button(self, text="back to shopping",
                            command=lambda: controller.show_frame(StartPage))

        button2.grid(row=5, column=8)

        button3 = tk.Button(self, text="Update user info",
                            command=lambda: self.update_info(controller))

        button3.grid(row=5, column=10)

    # Used refresh the information within the page
    def my_refresh(self, controller):

        if controller.user['cardnum'] != None:
            self.user_card_num_entry.delete(0, tk.END)
            self.user_card_num_entry.insert(tk.END, controller.user['cardnum'])
        if controller.user['ccv'] != None:
            self.user_card_ccv_entry.delete(0, tk.END)
            self.user_card_ccv_entry.insert(tk.END, controller.user['ccv'])
        if controller.user['expdate'] != None:
            self.user_card_exp_entry.delete(0, tk.END)
            self.user_card_exp_entry.insert(tk.END, controller.user['expdate'])
        if controller.user['country'] != None:
            self.user_country_entry.delete(0, tk.END)
            self.user_country_entry.insert(
                tk.END, controller.user['country'])
        if controller.user['province'] != None:
            self.user_province_entry.delete(0, tk.END)
            self.user_province_entry.insert(
                tk.END, controller.user['province'])
        if controller.user['streetaddress'] != None:
            self.user_adress_entry.delete(0, tk.END)
            self.user_adress_entry.insert(
                tk.END, controller.user['streetaddress'])
        if controller.user['city'] != None:
            self.user_city_entry.delete(0, tk.END)
            self.user_city_entry.insert(
                tk.END, controller.user['city'])
        if controller.user['postalcode'] != None:
            self.user_postal_entry.delete(0, tk.END)
            self.user_postal_entry.insert(
                tk.END, controller.user['postalcode'])

        orders = middleware.get_orders(controller.user['uid'])
        for child in self.orders_box.get_children():
            self.orders_box.delete(child)

        for order in orders:
            self.orders_box.insert("", "end", values=(
                order['oid'], order['shippedfrom'], order['currentlocation'], order['postalcode']))

    # calls the middleware function that will update the users information based on the information passed in
    def update_info(self, controller):
        temp = middleware.update_user(controller.user, self.user_card_num_entry.get(), self.user_card_ccv_entry.get(), self.user_card_exp_entry.get(
        ), self.user_country_entry.get(), self.user_province_entry.get(), self.user_adress_entry.get(), self.user_city_entry.get(), self.user_postal_entry.get())
        if temp == None:
            print("Failed Update")
            return
        controller.user = temp
        self.my_refresh(controller)

# page used to register a new user


class register_page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # enties to get the information needed to create a new user
        self.user_username_label = tk.Label(
            self, text="Username: ").grid(column=0, row=0)
        self.user_username_entry = tk.Entry(self)
        self.user_username_entry.grid(column=1, row=0)

        self.user_password_label = tk.Label(
            self, text="Password: ").grid(column=2, row=0)
        self.user_password_entry = tk.Entry(self)
        self.user_password_entry.grid(column=3, row=0)

        self.info_label = tk.Label(
            self, text="You may ignore the entries below if you would like").grid(column=0, columnspan=3, row=1)

        self.user_card_num_label = tk.Label(
            self, text="Card Number: ").grid(column=0, row=3)
        self.user_card_num_entry = tk.Entry(self)
        self.user_card_num_entry.grid(column=1, row=3)

        self.user_card_ccv_label = tk.Label(
            self, text="CCV: ").grid(column=2, row=3)
        self.user_card_ccv_entry = tk.Entry(self)
        self.user_card_ccv_entry.grid(column=3, row=3)

        self.user_card_exp_label = tk.Label(
            self, text="expiry date (MM/YY)").grid(column=4, row=3)
        self.user_card_exp_entry = tk.Entry(self)
        self.user_card_exp_entry.grid(column=5, row=3)

        self.user_country_label = tk.Label(
            self, text="Country: ").grid(column=6, row=3)
        self.user_country_entry = tk.Entry(self)
        self.user_country_entry.grid(column=7, row=3)

        self.user_province_label = tk.Label(
            self, text="Province: ").grid(column=0, row=4)
        self.user_province_entry = tk.Entry(self)
        self.user_province_entry.grid(column=1, row=4)

        self.user_city_label = tk.Label(
            self, text="City: ").grid(column=2, row=4)
        self.user_city_entry = tk.Entry(self)
        self.user_city_entry.grid(column=3, row=4)
        self.user_adress_label = tk.Label(
            self, text="Address: ").grid(column=4, row=4)
        self.user_adress_entry = tk.Entry(self)
        self.user_adress_entry.grid(column=5, row=4)

        self.user_postal_label = tk.Label(
            self, text="Postal Code: ").grid(column=6, row=4)
        self.user_postal_entry = tk.Entry(self)
        self.user_postal_entry.grid(column=7, row=4)

        self.error_box = tk.Label(self)
        self.error_box.grid(column=0, row=5)
        # button to register
        self.register_button = tk.Button(
            self, text="Register", command=lambda: self.register(controller))
        self.register_button.grid(column=0, row=6)

    def my_refresh(controller):
        print("place holder")

    # creates a new tuple in the users relation using the middleare function
    def register(self, controller):
        if self.user_username_entry != '' and self.user_password_entry.get() != '':
            new_user = middleware.register_user(self.user_username_entry.get(), self.user_password_entry.get(), self.user_card_num_entry.get(), self.user_card_ccv_entry.get(), self.user_card_exp_entry.get(
            ), self.user_country_entry.get(), self.user_province_entry.get(), self.user_adress_entry.get(), self.user_city_entry.get(), self.user_postal_entry.get())
            if new_user != None:
                controller.user = new_user
                controller.show_frame(StartPage)
            else:
                print("username or passowrd has been taken")
                self.error_box.config(text="USERNAME OR PASSWORD WAS TAKEN")

# page used to create the admin page


class admin_page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # box that will show all of the books in the database
        self.book_box = ttk.Treeview(self, columns=(
            'id', 'title', 'publisher', 'isbn', "authors", 'pages', "geners", 'price', 'quantity', 'shown'), show='headings')
        self.book_box.heading("id", text="id")
        self.book_box.column('id', width=0, minwidth=0)

        self.book_box.heading("title", text="title")
        self.book_box.heading("publisher", text="Publisher")
        self.book_box.heading("isbn", text="isbn")
        self.book_box.heading("authors", text="author(s)")
        self.book_box.heading("pages", text="pages")
        self.book_box.heading("price", text="price")
        self.book_box.heading("geners", text="geners")
        self.book_box.heading("quantity", text="quantity")
        self.book_box.heading("shown", text="Shown")
        self.book_box.grid(column=0, columnspan=7, row=0, rowspan=2)

        # button to stop the selected book to be shown to the users
        self.remove_button = tk.Button(
            self, text="Remove OR add back, book to shop front", command=lambda: self.remove_book(controller))
        self.remove_button.grid(row=3, column=3)

        # shows all of the publishers
        self.publisher_box = ttk.Treeview(self, columns=(
            'id', 'name', 'email', 'address', "bankid", 'compansation'), show='headings')
        self.publisher_box.heading("id", text="id")

        self.publisher_box.heading("name", text="name")
        self.publisher_box.heading("email", text="email")
        self.publisher_box.heading("address", text="address")

        self.publisher_box.heading("bankid", text="bank id")
        self.publisher_box.heading("compansation", text="compensation")
        self.publisher_box.grid(column=0, columnspan=7, row=4)

        # entires to add to the new books to the database
        tk.Label(self, text=" ").grid(row=6, column=0)
        tk.Label(self, text="Title:").grid(column=0, row=7)
        self.title_entry = tk.Entry(self)
        self.title_entry.grid(column=1, row=7)

        tk.Label(self, text="Publisher Name:").grid(column=2, row=7)
        self.publisher_entry = tk.Entry(self)
        self.publisher_entry.grid(column=3, row=7)

        tk.Label(self, text="ISBN:").grid(column=4, row=7)
        self.isbn_entry = tk.Entry(self)
        self.isbn_entry.grid(column=5, row=7)

        tk.Label(self, text="Number of pages:").grid(column=6, row=7)
        self.page_entry = tk.Entry(self)
        self.page_entry.grid(column=7, row=7)

        tk.Label(self, text="Price:").grid(column=0, row=8)
        self.price_entry = tk.Entry(self)
        self.price_entry.grid(column=1, row=8)

        tk.Label(self, text="Percentage cut:").grid(column=2, row=8)
        self.percentage_entry = tk.Entry(self)
        self.percentage_entry.grid(column=3, row=8)

        tk.Label(self, text="Inital quantity:").grid(column=4, row=8)
        self.quantity_entry = tk.Entry(self)
        self.quantity_entry.grid(column=5, row=8)

        tk.Label(self, text="Author(s) (,):").grid(column=6, row=8)
        self.author_entry = tk.Entry(self)
        self.author_entry.grid(column=7, row=8)

        tk.Label(self, text="genre(s) (,):").grid(column=0, row=9)
        self.genres_entry = tk.Entry(self)
        self.genres_entry.grid(column=1, row=9)

        self.new_book = tk.Button(
            self, text="Add book", command=lambda: self.add_book(controller))
        self.new_book.grid(column=3, row=9)

        # to show the the revenue and expenditures
        self.rev_expend_label = tk.Label(self)
        self.rev_expend_label.grid(column=0, row=10)

        self.populate(controller)

    # populates all of the tables in the admin page
    def populate(self, controller):
        for child in self.book_box.get_children():
            self.book_box.delete(child)
        for publisher in self.publisher_box.get_children():
            self.publisher_box.delete(publisher)
        for new_book in controller.books:
            string = ""
            auth_string = ""
            for genre in controller.genres:
                if genre["bid"] == new_book['bid']:
                    string += genre["genre"] + " "

            for author in controller.authors:
                if (author["bid"] == new_book["bid"]):
                    auth_string += author["authname"] + " "
            self.book_box.insert("", 'end', values=(
                new_book['bid'], new_book['title'], new_book['publishername'], new_book['isbn'], auth_string, new_book['numpages'], string, new_book['price'], new_book["quantity"], new_book['show']))

        publishers = middleware.get_publishers()

        for pub in publishers:
            self.publisher_box.insert("", "end", values=(
                pub['pid'], pub['name'], pub['email'], pub['country']+", "+pub['province']+", "+pub['city']+", "+pub['streetaddress']+", "+pub['postalcode'], pub['bankid'], pub['compensation']))

        self.rev_expend_label.config(text=middleware.sum_costs_and_sales())

    # used to change the viewable state of the books
    def remove_book(self, controller):
        selected = self.book_box.selection()[0]
        middleware.update_shown(self.book_box.item(
            selected)['values'][0], self.book_box.item(selected)['values'][8])

        controller.refresh_vars()
        self.populate(controller)

    # used to add new books to the database
    def add_book(self, controller):
        if len(self.title_entry.get()) != 0 and len(self.publisher_entry.get()) != 0 and len(self.isbn_entry.get()) != 0 and 0 < int(
                self.page_entry.get()) and 0 < float(self.price_entry.get()) and 0 < float(self.percentage_entry.get()) and 0 < int(self.quantity_entry.get()) and len(self.author_entry.get().split(',')) > 0 and len(self.genres_entry.get().split(',')) > 0:
            middleware.add_book(self.title_entry.get(), self.publisher_entry.get(), self.isbn_entry.get(), int(
                self.page_entry.get()), float(self.price_entry.get()), float(self.percentage_entry.get()), int(self.quantity_entry.get()), self.author_entry.get().split(','), self.genres_entry.get().split(','))
        controller.refresh_vars()
        self.populate(controller)

        # Driver Code
app = tkinterApp()
#app.resizable(False, False)
app.title("Look Inna Book store")
# app.geometry('1280x720+50+50')
app.mainloop()

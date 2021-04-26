import requests
from bs4 import BeautifulSoup
from tkinter import *
from PIL import Image, ImageTk


class Tennis(Tk):               # Decided to make a class for the functions so that I can use variables from one function to another

    def __init__(self):

        self.URL = 'https://www.tennis.com/rankings/ATP/'          # this is the website that has the tennis rankings
        self.page = requests.get(self.URL)                         # this line gets the HTML data from the url and stores it in page

        self.soup = BeautifulSoup(self.page.content, 'html.parser')              # uses the BeautifulSoup module to parse the html data, now we can look for specific id's

        self.results = self.soup.find(id='atpRanking')             # when looking at the html data ( I viewed page source), all the player data is under this id

        self.tennis_rolodex = {}                                   # initializing a dictionary and lists to use later
        self.players = []
        self.curr_rank = []
        self.prev_rank = []
        self.country = []
        self.points = []

        self.player_elems = self.results.find_all('td', class_='player-name')                   # finds all the player names, but it still has html script around it

        for self.player_elem in self.player_elems:                                # goes through each players name, strips all the html script to leave only the players name then appends it to the players list
            self.players.append(self.player_elem.text.strip())

        self.curr_elems = self.results.find_all('td', class_='current-rank')      # The next few lines are doing the same thing, striping for just text and appending the strings into their respective lists

        for self.curr_elem in self.curr_elems:
            self.curr_rank.append(self.curr_elem.text.strip())

        self.prev_elems = self.results.find_all('td', class_='prev-rank')

        for self.prev_elem in self.prev_elems:
            self.prev_rank.append(self.prev_elem.text.strip())

        self.country_elems = self.results.find_all('span', class_='country-name')

        for self.country_elem in self.country_elems:
            self.country.append(self.country_elem.text.strip())

        self.points_elems = self.results.find_all('td', class_='player-points')

        for self.points_elem in self.points_elems:
            self.points.append(self.points_elem.text.strip())

        for i in range(80):
            self.tennis_rolodex[self.players[i]] = self.curr_rank[i], self.prev_rank[i], self.country[i], self.points[i]                      # for loop that fills the dictionary with the top 80 players, with the name as the key and the info as the values

        self.player_list = list(self.tennis_rolodex.keys())                     # makes a list of the top 80 players, will be used later


        self.window_maker()                        # starts the window function

    def window_maker(self):

        Tk.__init__(self)                   # make the tkinter window

        self.image = requests.get("https://cdn.squaremile.com/gallery/5cac5b255fc15.jpeg")              # using the request funtion again to get the jpeg image I want
        self.file = open("Wimbledon_Court.jpeg", "wb")                                                  # making a new jpeg file with the image inside
        self.file.write(self.image.content)
        self.file.close()

        self.geometry('1000x600')                       # making the window size

        self.court_img = Image.open('Wimbledon_Court.jpeg')                 # Using Pillow to resize the image to match the window and making it an image tkinter can read
        self.size = self.court_img.resize((1000, 600))
        self.background_image = ImageTk.PhotoImage(self.size)

        # Using the tkinter module to make the wimbledon image the background and adding title and entry text
        self.canvas = Canvas(self, height=600, width=1000)
        self.canvas.create_image((500, 300), image=self.background_image)
        self.canvas.create_text((500, 80), text='Welcome to the Tennis Rolodex', font='Fixedsys 20 bold',
                                fill='dark olive green')
        self.canvas.create_text((500, 105), text='the hub for player information', font='Fixedsys 16 bold',
                                fill='dark olive green')
        self.canvas.create_text((310, 240), text='First Name:', font='Fixedsys 16 bold', fill='dark olive green')
        self.canvas.create_text((310, 290), text='Last Name:', font='Fixedsys 16 bold', fill='dark olive green')
        self.canvas.pack()

        # putting instructions at the bottom left of the screen using Label()
        self.Instructions = Label(self,
                                  text='Instructions: Enter a Players name (first and last name, only the first letters capitalized) in the top 80 Rankings into the search bars and press Search',
                                  font='Verdana 8', fg='black', bg='white')
        self.Instructions.place(relx=0.0, rely=1.0, anchor='sw')

        # Making and placing the first name/last name search bars
        self.Search_bar1 = Entry(self)
        self.Search_bar1.place(x=380, y=220, width='250', height='40')

        self.Search_bar2 = Entry(self)
        self.Search_bar2.place(x=380, y=270, width='250', height='40')

        # Making the Search button, once its placed, it looks at "command=" and runs player_search()
        self.Search_button = Button(self, text='Search', font='bold', command=self.player_search, bg='dark olive green')
        self.Search_button.place(x=460, y=325, width='100', height='30')

    def player_search(self):

        first_name = self.Search_bar1.get()            # getting the first name and last name entries from the previous function
        last_name = self.Search_bar2.get()

        # edge case where they don't enter anything and press search
        if not first_name and not last_name:

            self.destroy()              # closes the first window

            # making a new backround(same process as last time, but with a new jpeg image)
            self.image2 = requests.get(
                "https://abingtonsports.com/images/2018/10/1/tennis_background.jpg?width=1023&quality=80&format=jpg")
            self.file = open("Court.jpg", "wb")
            self.file.write(self.image2.content)
            self.file.close()

            window2 = Tk(className='Error')               # the title of the window will be "Error"
            window2.geometry('1000x600')

            self.court_img2 = Image.open('Court.jpg')
            self.size2 = self.court_img2.resize((1000, 600))
            self.background_image = ImageTk.PhotoImage(self.size2)

            canvas2 = Canvas(window2, height=600, width=1000)
            canvas2.create_image((500, 300), image=self.background_image)
            canvas2.pack()

            # making the error message using Label()
            Error = Label(canvas2, text="Please enter a players name for the search to work, Thanks! Press Search Again to Try Again", fg='black', bg='brown', justify='center',
                              wraplength='650', font='Verdana 25 bold', relief='raised')
            Error.pack()
            canvas2.create_window(400, 250, window=Error)

            # Making the search button that when pressed does two things; destroys the current window and brings up the window maker function
            Search_button = Button(window2, text='Search Again', font='bold',
                                       command=lambda: [window2.destroy(), self.window_maker()], bg='black', fg='white')
            Search_button.place(x=350, y=380, width='180', height='40')

            return                    # so that the code outside of the conditional doesnt run

        # another edge case: if they leave one of the search bars blank
        if not first_name or not last_name:

            # every thing is essentially the same as the previous edge case, with a different error message in "text="

            self.destroy()

            self.image2 = requests.get(
                "https://abingtonsports.com/images/2018/10/1/tennis_background.jpg?width=1023&quality=80&format=jpg")
            self.file = open("Court.jpg", "wb")
            self.file.write(self.image2.content)
            self.file.close()

            window2 = Tk(className='Error')
            window2.geometry('1000x600')

            self.court_img2 = Image.open('Court.jpg')
            self.size2 = self.court_img2.resize((1000, 600))
            self.background_image = ImageTk.PhotoImage(self.size2)

            canvas2 = Canvas(window2, height=600, width=1000)
            canvas2.create_image((500, 300), image=self.background_image)
            canvas2.pack()

            Error = Label(canvas2,
                          text="Please enter a players first and last name for the search to work, Thanks! Press Search Again to Try Again",
                          fg='black', bg='brown', justify='center',
                          wraplength='650', font='Verdana 25 bold', relief='raised')
            Error.pack()
            canvas2.create_window(400, 250, window=Error)
            Search_button = Button(window2, text='Search Again', font='bold',
                                   command=lambda: [window2.destroy(), self.window_maker()], bg='black', fg='white')
            Search_button.place(x=350, y=380, width='180', height='40')

            return                   # so that the code outside of the conditional doesnt run

        # allows the user to still search even if they don't use a capital letter in first/last manes
        if first_name[0].islower():
            fnlist = list(first_name)               # make the string a list, capitalizes the first letter and makes it a string again
            fnlist[0] = first_name[0].upper()
            first_name = ''.join(fnlist)

        if last_name[0].islower():
            lnlist = list(last_name)
            lnlist[0] = last_name[0].upper()
            last_name = ''.join(lnlist)

        full_name = first_name + " " + last_name           # joins the first and last name to be able to search

        # Creating the background like in edge cases
        self.destroy()

        self.image2 = requests.get(
            "https://abingtonsports.com/images/2018/10/1/tennis_background.jpg?width=1023&quality=80&format=jpg")
        self.file = open("Court.jpg", "wb")
        self.file.write(self.image2.content)
        self.file.close()

        window2 = Tk(className='player information')                # the title of the window will be "Error"
        window2.geometry('1000x600')

        self.court_img2 = Image.open('Court.jpg')
        self.size2 = self.court_img2.resize((1000, 600))
        self.background_image = ImageTk.PhotoImage(self.size2)

        canvas2 = Canvas(window2, height=600, width=1000)
        canvas2.create_image((500, 300), image=self.background_image)
        canvas2.pack()

        # searches for the name in the top 80 list, if in the list it makes a label with all the information, and gives them the chance to search again.
        # if not in the list, it shows an error message and allow them to search again.

        if full_name in self.player_list:
            name = Label(canvas2, text=full_name, fg='black', bg='white', font='Verdana 20 bold', relief='raised')
            name.pack()
            canvas2.create_window((500, 45), window=name)
            info = Label(canvas2,
                          text="Current Rank: " + self.tennis_rolodex[full_name][0] + '\n'*2 + "Previous Rank: " + self.tennis_rolodex[full_name][1] + '\n'*2
                               + "Country of Birth: " + self.tennis_rolodex[full_name][2] + '\n'*2 + "Total Points: " + self.tennis_rolodex[full_name][3],
                          fg='white', bg='dark green', justify='left', font='Verdana 25 bold', relief='raised', padx=28, pady=28)
            info.pack()
            canvas2.create_window(350, 280, window=info)

            # Making the search button that when pressed does two things; destroys the current window and brings up the window maker function
            Search_button = Button(window2, text='Search Again', font='bold',
                                   command=lambda: [window2.destroy(), self.window_maker()], bg='black', fg='white')
            Search_button.place(x=260, y=480, width='180', height='40')
        else:
            Error = Label(canvas2,
                          text="Sorry, the player you searched is not in the top 80 rankings, or you may have spelled their name incorrectly. "
                               "Press Search Again to Try Again", fg='black', bg='brown', justify='center',
                          wraplength='650', font='Verdana 25 bold', relief='raised', padx=20, pady=20)
            Error.pack()
            canvas2.create_window(400, 250, window=Error)

            # Making the search button that when pressed does two things; destroys the current window and brings up the window maker function
            Search_button = Button(window2, text='Search Again', font='bold',
                                   command=lambda: [window2.destroy(), self.window_maker()], bg='black', fg='white')
            Search_button.place(x=320, y=400, width='150', height='40')


if __name__ == "__main__":
    app = Tennis()
    app.mainloop()      # keeps the windows up, without it the window would open and close in a fraction of a second

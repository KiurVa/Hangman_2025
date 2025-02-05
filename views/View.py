from tkinter import *
from tkinter import font, messagebox
from tkinter.ttk import Combobox

from PIL import ImageTk, Image


class View(Tk):
    def __init__(self, model): #Tuleb anda model kaasa
        super().__init__() #See on Tk jaoks. Et oleks põhiine view
        self.model = model #app.py failis loodud model

        #Põhiakna omadused
        self.__width = 585 #Privaatne muutuja akna laius
        self.__height = 200 #Privaatne muutuja akna kõrgus. __ei luba muuta kõrgust ja laiust
        self.title('Poomismäng 2025') #Tiitelriba tekst
        self.center(self, self.__width, self.__height) #Paiguta põhiaken keskele, kaasa view ja andmed

        #Kirjastiilid
        self.__big_font =  font.Font(family='Courier', size=20, weight='bold') #Tekst kollasel taustal
        self.__default = font.Font(family='Verdana', size=12) # Vaikimisi kirjastiil (lbl - label, btn - button)
        self.__default_bold = font.Font(family='Verdana', size=12, weight='bold') #Vaikimis rasvane tekst (valesti pakutud tähed)

        #Kogu vormi stiil
        self.option_add('*Font', self.__default) #Määrab font on default

        #Loob kolm paneeli(Frame)
        self.__frame_top, self.__frame_bottom, self.__frame_image = self.create_frames()

        #Loob neli nuppu
        self.__btn_new, self.__btn_scoreboard, self.__btn_cancel, self.__btn_send = self.create_buttons()

        #Loob pildi "koha"
        self.__image = ImageTk.PhotoImage(Image.open('images/hang11.png'))
        self.__lbl_image = None

        #Loob "kolm" labelit
        self.__lbl_error, self.__lbl_time, self.__lbl_result = self.create_labels()

        #Loob rippmenüü
        self.__cmb_category = self.create_combobox() #cmb - combobox - rippmenüü

        #Loob sisestuskasti
        self.__char_input = self.create_entry()


    @staticmethod
    def center(win, width, height): #Arvutab ekraani suuruse põhjal keskele akna
        x = int((win.winfo_screenwidth() / 2) - (width / 2))
        y = int((win.winfo_screenheight() / 2) - (height / 2))
        win.geometry(f'{width}x{height}+{x}+{y}')

    def create_frames(self):
        top = Frame(self, height = 50, background = 'lightblue')
        bottom = Frame(self, background = 'lightyellow')
        image = Frame(top, background = 'lightsalmon', width=130, height=130)

        #Paiguta paneelid põhiaknale
        top.pack(fill=BOTH)
        bottom.pack(fill=BOTH, expand=True)
        image.grid(row=0, column=3, padx=5, pady=5, rowspan=4) #Rida üks ja neljas veerg, üle nelja rea(ühendab neli rida)
        return top, bottom, image #Tagastab vidinad

    def create_buttons(self):
        new = Button(self.__frame_top, text='Uus mäng')
        scoreboard = Button(self.__frame_top, text='Edetabel')
        cancel = Button(self.__frame_top, text='Katkesta', state=DISABLED)
        send = Button(self.__frame_top, text='Saada', state=DISABLED)
        new.grid(row=0, column=0, padx=5, pady=2, sticky=EW) #Sticky venitab veeru nii laiaks kui neid on
        scoreboard.grid(row=0, column=1, padx=5, pady=5, sticky=EW)
        cancel.grid(row=0, column=2, padx=5, pady=2, sticky=EW)
        send.grid(row=2, column=2, padx=5, pady=2, sticky=EW)
        return new, scoreboard, cancel, send

    def create_labels(self):
        #Labelid, mille tulemusi ei saa muuta.
        Label(self.__frame_top, text='Kategooria').grid(row=1, column=0, padx=5, pady=2, sticky=EW)
        Label(self.__frame_top, text='Sisesta täht').grid(row=2, column=0, padx=5, pady=2, sticky=EW)
        #Loob labelid Error, Time, Result
        error = Label(self.__frame_top, text='Vigased tähed', anchor=W, font=self.__default_bold) #Joondatakse lahtri vasakule serve W = West
        time = Label(self.__frame_top, text='00:00:00')
        result = Label(self.__frame_bottom, text='m _ _ _ _ m _'.upper(), font=self.__big_font, background='lightyellow')
        error.grid(row=3, column=0, padx=5, pady=2, columnspan=3, sticky=EW)
        time.grid(row=1, column=2, padx=5, pady=2, sticky=EW)
        result.pack(pady = 10)
        #Pildi panek
        self.__lbl_image = Label(self.__frame_image, image=str(self.__image))
        self.__lbl_image.pack()
        return error, time, result

    def create_combobox(self):
        combo = Combobox(self.__frame_top, state='readonly')
        combo['values'] = self.model.categories
        combo.current(0)
        combo.grid(row=1, column=1, padx=5, pady=2, sticky=EW)
        return combo

    def create_entry(self):
        char = Entry(self.__frame_top, justify='center')
        char['state'] = 'disabled'
        char.focus()
        char.grid(row=2, column=1, padx=5, pady=2, sticky=EW)
        return char

    @staticmethod
    def show_message(message):
        root = Tk()
        root.withdraw()  # Peidab loodava akna
        messagebox.showerror("Viga", message=f'{message}')
        #root.destroy()
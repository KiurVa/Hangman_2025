import random
from tkinter import simpledialog, messagebox
from tkinter.constants import DISABLED, NORMAL

from models.Database import Database
from models.Leaderboard import Leaderboard
from models.Stopwatch import Stopwatch
from models.Timer import Timer
from views.View import View


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.stopwatch = Stopwatch(self.view.lbl_time)

        #Ajasti loomine
        self.timer = Timer(
            scheduled_callback=self.view.after,
            cancel_callback=self.view.after_cancel,
            interval=5000, #5sek
            callback=self.change_title,
        )

        """Nuppude callback seaded"""
        self.btn_new_callback()
        self.btn_cancel_callback()
        self.btn_send_callback()
        self.btn_scoreboard_callback()
        self.view.set_timer_reset_callback(self.reset_timer) #Ajasti värk

        #Enter klahvi funktsionaalsus


    def buttons_for_game(self):
        #Nupud mängu hetkel, mis klikitav jms
        self.view.btn_new['state'] = DISABLED
        self.view.btn_send['state'] = NORMAL
        self.view.btn_cancel['state'] = NORMAL
        self.view.char_input['state'] = NORMAL
        self.view.char_input.focus()
        self.view.cmb_category['state'] = DISABLED


    def buttons_for_not_game(self):
        """Kui vajutatakse katkestamis nuppu"""
        self.view.btn_new['state'] = NORMAL
        self.view.btn_send['state'] = DISABLED
        self.view.btn_cancel['state'] = DISABLED
        self.view.char_input.delete(0, 'end') #Tühjendab sisestuskasti enne Disablet
        self.view.char_input['state'] = DISABLED
        self.view.cmb_category['state'] = NORMAL

    def btn_new_callback(self):
        self.view.set_button_new_callback(self.btn_new_click) #Meetod ilma sulgudeta

    def btn_cancel_callback(self):
        self.view.set_button_cancel_callback(self.btn_cancel_click)

    def btn_send_callback(self):
        self.view.set_btn_send_callback(self.btn_send_click)

    def btn_scoreboard_callback(self):
        self.view.set_btn_scoreboard_callback(self.btn_scoreboard_click)

    def btn_cancel_click(self):
        self.buttons_for_not_game()
        self.stopwatch.stop()
        self.timer.stop() #Peatab title juhuslikkuse
        self.view.lbl_result.config(text=self.model.user_word)
        self.view.title(self.model.titles[0]) #Paneb listi esimese sõna titleks

    def btn_new_click(self):
        self.buttons_for_game() #Nupu majandus - peidus jms
        #Seadista juhuslik sõna ja asendab tähed _
        self.model.start_new_game(self.view.cmb_category.current(), self.view.cmb_category.get()) #id, sõna. Leiab dictist
        #Näitab sõna allkriipse konsoolis
        self.view.lbl_result.config(text=self.model.user_word)
        #Vigased tähed reset
        self.view.lbl_error.config(text='Vigased tähed', fg='black')
        self.view.change_image(self.model.counter) #Kas see või 0 sulgudes
        self.timer.start() #Käivitab title juhuslikkuse
        self.stopwatch.reset() #Eelmise mängu reset
        self.stopwatch.start() #Paneb aja tööle
        self.view.bind('<Return>', lambda event: self.btn_send_click()) #Teeb enter klahvi aktiivseks

    def btn_send_click(self):
        self.model.get_user_input(self.view.char_input.get().strip()) #Saada sisestus.
        self.view.lbl_result.config(text=self.model.user_word) #Uuenda tulemust.
        self.view.lbl_error.config(text=f'Vigased tähed {self.model.get_all_user_chars()}')
        self.view.char_input.delete(0, 'end')
        if self.model.counter > 0: #Kontrollime kas on vigu ja teeme vajalikud muudatused
            self.view.lbl_error.config(fg='red')
            self.view.change_image(self.model.counter)
        self.is_game_over() #Kontrollib kas mmäng on läbi

    def btn_scoreboard_click(self):
        """Edetabeli nupu toimime, kui edetabel tühi ja kui data on olemas"""
        data = self.model.read_leaderboard()
        if not data:
            View.show_message('Edetabel on tühi')
        else:
            popup_window = self.view.create_popup_window()
            self.view.generate_scoreboard(popup_window, data)

    def is_game_over(self): #Mängu lõpetamise ülesanded
        if self.model.counter >= 11 or '_' not in self.model.user_word:
            self.stopwatch.stop()
            self.timer.stop()  # Peatab title juhuslikkuse
            self.buttons_for_not_game() #Nupud muutuvad selliseks, et saaks uuesti alustada
            player_name = simpledialog.askstring('Mäng on läbi', 'Kuidas on mängija nimi?', parent=self.view)
            messagebox.showinfo('Teade', 'Oled lisatud edetabelisse.')
            self.model.save_player_score(player_name, self.stopwatch.seconds)
            self.view.title(self.model.titles[0]) #Paneb listi esimese sõna titleks
            self.view.unbind('<Return>')  # lõpetab enter klahvi töö

    def change_title(self):
        new_title = random.choice(self.model.titles)
        self.view.title(new_title)

    def reset_timer(self):
        self.timer.start()
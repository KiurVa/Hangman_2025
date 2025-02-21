import sys

from controllers.Controller import Controller
from models.Database import Database
from models.Model import Model
from views.View import View

if __name__ == "__main__":
    try:
        db = Database()
        model =  Model()
        view = View(model) #Loo view andes kaasa model
        Controller(model, view)
        view.mainloop() #Viimane rida koodis
    except FileNotFoundError as e:
        #print(f'Viga: {e}')
        View.show_message(e) #Kutsub meetodi View.show_message
        sys.exit(1)
    except ValueError as e:
        View.show_message(e)
        sys.exit(1)
    except Exception as e:
        #print(f'Tekkis ootamatu viga: {e}')
        View.show_message(e) #Kutsub meetodi View.show_message
        sys.exit(1)
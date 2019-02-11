class BaseEncoder:
    def __init__(self, orientation: "E or W", max_step):
        self.current_step = 0
        self.__motion_step__ = 0
        self.__min_step__ = 0
<<<<<<< HEAD
        self.__max_step__ = 350
=======
        self.__max_step__ = max_step
>>>>>>> f19c84bcc05c5b87a54970b954553cb414275d89
        self.orientation = orientation


    def listen_until(self, length):

        """resta in ascolto sul valore corrente dell'encoder finché non viene percorsa tutta la differenza indicata"""

        if length > self.current_step or length == self.__max_step__:
            direction = "F"
        elif length < self.current_step or length == self.__min_step__:
            direction = "B"
        else:
            raise ValueError("Errore misurazione")

        while(self.__condition__(length, direction)):
            self.__save_current_step__(direction)

        self.current_step = self.__motion_step__
        print("step corrente dell'encoder "+self.orientation+": "+str(self.current_step))

    def __condition__(self, length, direction):

        """Verifica se la condizione per uscire dal ciclo è avvenuta"""

        if direction == "F":
            if self.__motion_step__ == self.__max_step__:
                return False
            condition = length > self.__motion_step__
        elif direction == "B":
            if self.__motion_step__ == self.__min_step__:
                return False
            condition = length < self.__motion_step__
        return condition

    def __save_current_step__(self, direction):
        """
            solo questo metodo andrebbe implementato diversamente nella classe che comunica con l'encoder reale:
            si dovrebbe lusare RPi.GPIO per andare a leggere l'hardware e aggiornare di conseguenza il valore degli step
        """
        raise NotImplementedError()

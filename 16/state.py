class State:
    def handle_input(self, server, client_socket, command):
        raise NotImplementedError("Tuto metodu musí implementovat konkrétní stav.")

class StateKnowNothing(State):
    def handle_input(self, server, client_socket, command):
        if command == "ex":
            server.state = None
            return "Vracíte se do standardního režimu."
        if "=" in command:
            key, value = command.split("=")
            if key == "U":
                server.state = StateKnowU(float(value.replace("k", "e3").replace("m", "e-3")))
                return "OK"
            elif key == "R":
                server.state = StateKnowR(float(value.replace("k", "e3").replace("m", "e-3")))
                return "OK"
            elif key == "I":
                server.state = StateKnowI(float(value.replace("k", "e3").replace("m", "e-3")))
                return "OK"
        elif command == "U=?":
            return "Nemám dostatek informací."
        elif command == "R=?":
            return "Nemám dostatek informací."
        elif command == "I=?":
            return "Nemám dostatek informací."
        return "Neplatný příkaz."

class StateKnowU(State):
    def __init__(self, U):
        self.U = U

    def handle_input(self, server, client_socket, command):
        if command == "ex":
            server.state = None
            return "Vracíte se do standardního režimu."
        if "=" in command:
            key, value = command.split("=")
            if key == "R":
                server.state = StateKnowRandU(self.U, float(value.replace("k", "e3").replace("m", "e-3")))
                return "OK"
            elif key == "I":
                server.state = StateKnowUandI(self.U, float(value.replace("k", "e3").replace("m", "e-3")))
                return "OK"
        elif command == "U=?":
            return f"U={self.U}V"
        elif command == "R=?":
            return "Nemám dostatek informací."
        elif command == "I=?":
            return "Nemám dostatek informací."
        return "Neplatný příkaz."

class StateKnowR(State):
    def __init__(self, R):
        self.R = R

    def handle_input(self, server, client_socket, command):
        if command == "ex":
            server.state = None
            return "Vracíte se do standardního režimu."
        if "=" in command:
            key, value = command.split("=")
            if key == "U":
                server.state = StateKnowRandU(float(value.replace("k", "e3").replace("m", "e-3")), self.R)
                return "OK"
            elif key == "I":
                server.state = StateKnowRandI(self.R, float(value.replace("k", "e3").replace("m", "e-3")))
                return "OK"
        elif command == "R=?":
            return f"R={self.R}Ω"
        elif command == "U=?":
            return "Nemám dostatek informací."
        elif command == "I=?":
            return "Nemám dostatek informací."
        return "Neplatný příkaz."

class StateKnowI(State):
    def __init__(self, I):
        self.I = I

    def handle_input(self, server, client_socket, command):
        if command == "ex":
            server.state = None
            return "Vracíte se do standardního režimu."
        if "=" in command:
            key, value = command.split("=")
            if key == "U":
                server.state = StateKnowUandI(float(value.replace("k", "e3").replace("m", "e-3")), self.I)
                return "OK"
            elif key == "R":
                server.state = StateKnowRandI(float(value.replace("k", "e3").replace("m", "e-3")), self.I)
                return "OK"
        elif command == "I=?":
            return f"I={self.I}A"
        elif command == "U=?":
            return "Nemám dostatek informací."
        elif command == "R=?":
            return "Nemám dostatek informací."
        return "Neplatný příkaz."

class StateKnowRandU(State):
    def __init__(self, U, R):
        self.U = U
        self.R = R

    def handle_input(self, server, client_socket, command):
        if command == "ex":
            server.state = None
            return "Vracíte se do standardního režimu."
        if command == "I=?":
            I = self.U / self.R
            return f"I={I}A"
        elif command == "U=?":
            return f"U={self.U}V"
        elif command == "R=?":
            return f"R={self.R}Ω"
        return "Neplatný příkaz."

class StateKnowRandI(State):
    def __init__(self, R, I):
        self.R = R
        self.I = I

    def handle_input(self, server, client_socket, command):
        if command == "ex":
            server.state = None
            return "Vracíte se do standardního režimu."
        if command == "U=?":
            U = self.R * self.I
            return f"U={U}V"
        elif command == "R=?":
            return f"R={self.R}Ω"
        elif command == "I=?":
            return f"I={self.I}A"
        return "Neplatný příkaz."

class StateKnowUandI(State):
    def __init__(self, U, I):
        self.U = U
        self.I = I

    def handle_input(self, server, client_socket, command):
        if command == "ex":
            server.state = None
            return "Vracíte se do standardního režimu."
        if command == "R=?":
            R = self.U / self.I
            return f"R={R}Ω"
        elif command == "U=?":
            return f"U={self.U}V"
        elif command == "I=?":
            return f"I={self.I}A"
        return "Neplatný příkaz."

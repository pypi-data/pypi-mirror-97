from .opendaprequest import OpeNDAPRequest
from .gui import GUI


def run():
    '''
    Launches the GUI-based application.
    '''
    # Constructor for GUI class accepts an instance
    # of OpeNDAPRequest class
    app = GUI(OpeNDAPRequest())
    app.mainloop()

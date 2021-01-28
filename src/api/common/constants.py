from os import path

CONSTANTS = {
    "DATABASE_PATH": path.abspath(path.join(path.dirname(__file__),
                                            "../../ticket.db"))
}
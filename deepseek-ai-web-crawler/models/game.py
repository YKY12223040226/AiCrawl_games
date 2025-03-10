from pydantic import BaseModel


class game(BaseModel):
    """
    Represents the data structure of a game.
    """

    name: str
    rating: float
    type: str
    descripration:str


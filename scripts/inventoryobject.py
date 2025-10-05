class InventoryObject():

    def __init__(self, id:str, name:str, description:str = "", image = None):
         self.id = id
         self.name = name
         self.description = description
         self.image = image
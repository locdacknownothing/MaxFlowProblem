class Node:
    def __init__(self, name, lat, lon):
        self.name = name
        self.lat = lat
        self.lon = lon
    
    def __repr__(self):
        return f"<Node(\n\tname={self.name}, \n\tlat={self.lat}, \n\tlon={self.lon}\n)>"
    
    def __str__(self):
        return self.__repr__()
    
    def __hash__(self):
        return hash(self.name)
    
    def __eq__(self, other):
        return isinstance(other, Node) and self.name == other.name
    
    def to_dict(self):
        return {
            "name": self.name,
            "lat": self.lat,
            "lon": self.lon,
        }

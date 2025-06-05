#Jacob Newell
#011742870


class HashMap:
    #create hashmap and functions, please see below:
    #taken from course resources / chatter/ tips from popular youtube video other students have used / recommended, this code is not my own!

    def __init__(self):
        self.size = 40
        self.map = [None] * self.size
    #key for items
    def _get_hash(self, key):
        hash = 0
        for char in str(key):
            hash += ord(char)
        return hash % self.size
    #add item to hashmap
    def add(self, key, value):
        key_hash = self._get_hash(key)
        key_value = [key, value]

        if self.map[key_hash] is None:
            self.map[key_hash] = [key_value]
            return True
        else:
            for pair in self.map[key_hash]:
                if pair[0] == key:
                    pair[1] = value  # Update existing key
                    return True
            self.map[key_hash].append(key_value)  # Handle collision
            return True
    #get item in hashmap
    def get(self, key):
        key_hash = self._get_hash(key)
        if self.map[key_hash] is not None:
            for pair in self.map[key_hash]:
                if pair[0] == key:
                    return pair[1]
        return None

    #delete item
    def delete(self, key):
        key_hash = self._get_hash(key)
        if self.map[key_hash] is None:
            return False
        for i in range(len(self.map[key_hash])):
            if self.map[key_hash][i][0] == key:
                self.map[key_hash].pop(i)
                return True
        return False
    #display hashtable
    def display(self):
        for item in self.map:
            if item is not None:
                print(str(item))


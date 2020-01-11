class Params:
    def __init__(self, trait, filter, arg):
        self.__trait = trait
        self.__filter = filter
        self.__arg = arg
    def get_trait(self):
        return self.__trait
    def set_trait(self, trait):
        self.__trait = trait
    def get_filter(self):
        return self.__filter
    def set_filter(self, filter):
        self.__filter = filter
    def get_arg(self):
        return self.__arg
    def set_arg(self, arg):
        self.__arg = arg

p = Params("none", (lambda x: x), "")

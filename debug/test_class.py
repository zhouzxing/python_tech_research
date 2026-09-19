class Class:
    name = 'Class'

    def __init__(self, at):
        self.attribute = at

    def change(self, ano):
        self.attribute = ano
        self.name = ano
        self.__class__.name = ano


    def change_obj(self, ano):
        self.attribute = ano
        self.name = ano


clazz = Class('abc')
print(clazz.name)

# clazz.change('good')
# print(Class.name, clazz.name, clazz.attribute)
clazz.change_obj('good')
print(Class.name, clazz.name, clazz.attribute)
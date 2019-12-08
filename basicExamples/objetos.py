import objetos

my_list = ['aa', 'bvbbb', 1, 3, 1.524, 1+4j, [1, 1], 3]
my_dict = {'cat': 'meow', 'dog': 'woof', 'cow': 'moo'}
my_2D_list = [[12, 1, 'a', '3'], [100, 1+4j, 3], ['asdf', 'ksdf']]

objetos.check_types(my_list)
print(objetos.get_int_list(my_list))
objetos.iterate_dict(my_dict)
print(objetos.flatten_2D_list(my_2D_list))
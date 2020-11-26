lista_productos = {
    "huevos":[5,[1,2,3,4]],
    "leche":[10, [1,2,3,4]],
    "carne":[15,[2,3]],
    "barbacoa":[15,[4]],
    "iratxe":[5,[1]],
    "pescado":[30,[1,4]],
    "alvar":[50,[2,3,4]],
}

lista_usuarios = {
    1:0,
    2:0,
    3:0,
    4:0,
}

for user in lista_usuarios.keys():
    lista_usuarios.get(user)
    for product in lista_productos.keys():
        if user in lista_productos.get(product)[1]:
            lista_usuarios[user] = lista_usuarios[user] + lista_productos.get(product)[0]/len(lista_productos.get(product)[1])

print(str(lista_usuarios))
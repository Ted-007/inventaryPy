from typing import List, Tuple
from abc import ABC, abstractmethod

class Product:
    def __init__(self, nombre: str, referencia: str, cantidad: int):
        self.nombre = nombre
        self.referencia = referencia
        self.cantidad = cantidad

    def __str__(self):
        return f"*********************\n" \
               f"Nombre: {self.nombre}\n" \
               f"Referencia: {self.referencia}\n" \
               f"Cantidad: {self.cantidad}\n" \
               f"**********************\n"

class Pila():
    def __init__(self, s: int, types: str):
        self.tope = 0
        self.size = s
        self.lista = []
        self.type = types

    @abstractmethod
    def getOrden(self):
        pass

    def addProduct(self, nombre: str, referecia: str, cantidad: str):
        if self.tope < self.size:
            stringStream = self.procesar(self.lista, referecia, cantidad)
            if not self.addValidation(stringStream):
                nuevo = [referecia, cantidad, nombre]
                print("producto agregado")
                self.lista.append(nuevo)
            self.tope += 1
        else:
            print(f"La Pila de {self.type} se Encuentra llena")

    def addValidation(self, stringStream):
        return any(s == "Elemento procesado" for s in stringStream)

    def removeOrEditProduct(self, referecia: str, cantidad: str):
        state = ""
        if self.covacio():
            print(f"No existen Facturas de {self.type} a Ejecutar")
        else:
            if cantidad is not None:
                self.lista = [product for product in self.lista if not product[0].equalsIgnoreCase(referecia)]
            else:
                self.procesar(self.lista, referecia, cantidad)
            self.tope -= 1
        return state

    def procesar(self, lista, referecia: str, cantidad: str):
        return (self.modify_product(product, referecia, cantidad) for product in lista)

    def modify_product(self, product, referecia: str, cantidad: str):
        print("entra ciclo de modificar stock")
        if product[0].equalsIgnoreCase(referecia):
            product[1] = cantidad
            return "Elemento procesado"
        return "Elemento no procesado"

    def covacio(self):
        return self.tope == 0

class PilaCompras(Pila):
    def __init__(self, s: int):
        super().__init__(s, "Compras")

    def getOrden(self):
        print("Orden de compra generada: ")
        print("___________________________________")
        numProdut = 0
        for s in self.lista:
            numProdut += 1
            print(f"producto nro: {numProdut}")
            print("*********************\n"
                  f"Nombre: {s[2]}\n"
                  f"Referencia: {s[0]}\n"
                  f"Cantidad: {s[1]}\n"
                  "**********************\n")
        print("___________________________________")

class PilaVentas(Pila):
    def __init__(self, s: int):
        super().__init__(s, "Ventas")

    def getOrden(self):
        print("Factura de venta generada: ")
        print("___________________________________")
        numProdut = 0
        for s in self.lista:
            numProdut += 1
            print(f"producto nro: {numProdut}")
            print("*********************\n"
                  f"Nombre: {s[2]}\n"
                  f"Referencia: {s[0]}\n"
                  f"Cantidad: {s[1]}\n"
                  "**********************\n")
        print("___________________________________")

def main():
    opc = ''
    val = False
    active = True
    products = []
    pilaCompras = PilaCompras(10)
    pilaVentas = PilaVentas(10)
    productBase(products)

    while active:
        clearScreen()
        print("\nMenu Principal")
        print("................\n")
        print("1 Articulos del Inventario")
        print("2 Ordenes de Compras")
        print("3 Facturas de Ventas")
        print("4 Reportes del Sistema")
        print("5 Salida del Sistema")

        opc = input("\nIngrese la Opcion a ejecutar: ")[0]

        val = opc.isdigit() and opc >= '1' and opc <= '5'
        if val:
            opcInt = int(opc)

            if opcInt >= 1 and opcInt <= 5:
                if opcInt == 1:
                    if val:
                        print("\nInventario")
                        print("___________________________________")
                        numProdut = 0
                        for product in products:
                            numProdut += 1
                            print(f"producto nro: {numProdut}")
                            print(product)
                        print("___________________________________")
                elif opcInt == 2:
                    print("2 Ordenes de Compras")
                    initializeProcess(pilaCompras, opc, val, products)
                elif opcInt == 3:
                    print("3 Facturas de Ventas")
                    initializeProcess(pilaVentas, opc, val, products)
                elif opcInt == 4:
                    print("4 Reportes del Sistema")
                    pilaVentas.getOrden()
                    pilaCompras.getOrden()
                elif opcInt == 5:
                    print("Salida exitosa del sistema")
                    active = False
            else:
                print("la opción ingresada no es valida: " + opcInt)
                active = True

def initializeProcess(pila, opc, val, products):
    activeProcess = True
    while activeProcess:
        if pila.lista:
            pila.getOrden()
        print("\nIngrese la Opcion a ejecutar: ")
        print("1 agregar")
        print("2 eliminar")
        opcSellorBuild = input()
        print("\nIngrese la referencia del producto: ")
        product = input()
        print("\nIngrese la cantidad del producto: ")
        count = input()
        if opcSellorBuild == "1":
            if pila.type == "Compras":
                print("\nIngrese el nombre del producto: ")
                name = input()
                pila.addProduct(name, product, count)
            else:
                validateExistProduct(products, count, product)
                pila.addProduct(None, product, count)
        elif opcSellorBuild == "2":
            if pila.lista:
                pila.removeOrEditProduct(product, count)
                print("\nproducto procesado")
            else:
                print("\n>>>>>>>>sin productos en la Pila<<<<<<<<")
        else:
            print("\nOpción no valida: " + opcSellorBuild)
        print("\nsi desea cerrar la operación digite la opción: (1)")
        print("\nde lo contrario marque (0)")
        terminate = input()
        if terminate == "1":
            modifyStock(pila, products)
            activeProcess = False

def modifyStock(pila, products):
    if not pila.lista:
        addProduct = [True]
        for s in pila.lista:
            for product in products:
                if product.referencia == s[0]:
                    addProduct[0] = False
                    if pila.type == "Compras":
                        product.cantidad += int(s[1])
                        print("\nStock actulizado con una compra")
                    else:
                        product.cantidad -= int(s[1])
                        print("\nStock actulizado con una venta")
                    break
            if addProduct[0] and pila.type == "Compras":
                products.append(Product(s[2], s[0], int(s[1])))


def validateExistProduct(products, count, product):
    allowCount = (product1 for product1 in products if product1.referencia.equalsIgnoreCase(product))
    productExists = next(allowCount, None)
    if productExists:
        if productExists.cantidad > int(count):
            print("\nproducto procesado")
        else:
            print("\nCantidad no disponible")
            # ingresar de nuevo el producto
    else:
        print("\nProducto no valido: ")
        # ingresar de nuevo el producto


def productBase(products):
    products.append(Product("cepillo", "1", 5))
    products.append(Product("enjuague bucal", "2", 5))
    products.append(Product("crema", "3", 5))
    products.append(Product("shampoo", "4", 5))
    products.append(Product("bloqueador", "5", 5))


def clearScreen():
    print("\033[H\033[2J")
    print("\033[H\033[2J", end="")


if __name__ == "__main__":
    main()

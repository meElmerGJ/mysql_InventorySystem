from queries import *


def close_program():
    print("\n\n\n\tPROGRAMA FINALIZADO")
    exit()


if __name__ == '__main__':
    try:
        create_tables()
        try:
            generate_data()
        except mysql.connector.errors.IntegrityError:
            pass

        print("\n\n\t\tSISTEMA DE INVENTARIO 1.0")

        while True:
            try:
                print("\n\n\nIngrese una opcion")
                print("1. Articulos\t2. Categorias\t3. Proveedores\t4. Transacciones\t5. Salir")
                op = input("\n>> ")

                match int(op):
                    # Operation for PRODUCT MODULE
                    case 1:
                        end = False
                        print("\n\n\n\tMODULO ARTICULOS\n")
                        while not end:
                            print("\n\nIngrese una opcion")
                            print("1. Nuevo\t2. Editar\t3. Buscar\t4. Eliminar\t5. Ver Articulos\t6. Salir")
                            op = input(">> ")
                            match int(op):
                                case 1:  # Add a product
                                    if new_product():
                                        print("\n\tPALABRA AGREGADA")

                                case 2:  # Edit a product
                                    value = input("ID de Producto a editar >> ")
                                    col = input("\nQue desea editar...?\n\t1. Nombre\t2. Categoria ID\t3. Proveedor ID\t4. Cantidad\t5. Cantidad "
                                                "Minima\t6. Precio\n>> ")
                                    new_value = input("Nuevo valor >> ")
                                    edit_product(value, col, new_value)

                                case 3:  # Search a product
                                    value = input("Ingrese nombre de articulo: ")
                                    get_product(value)

                                case 4:  # Delete a product
                                    value = input("Ingrese nombre de articulo: ")
                                    del_product(value)
                                    print("\n\tPALABRA ELIMINADA")

                                case 5:  # Get all products
                                    get_products()

                                case 6:  # Exit from module
                                    end = True

                    # Other cases...
                    case 2:
                        print("\n\n\n\tMODULO CATEGORIAS\n")
                        print("Ingrese una opcion\n1. Ver categorias")
                        op = input(">> ")
                        if op == '1':
                            get_categories()
                    case 3:
                        print("\n\n\n\tMODULO PROVEEDORES\n")
                        print("Ingrese una opcion\n1. Ver proveedores")
                        op = input(">> ")
                        if op == '1':
                            get_suppliers()
                    case 4:
                        print("\n\n\n\tMODULO TRANSACCIONES\n")
                        print("Ingrese una opcion\n1. Ver transacciones")
                        op = input(">> ")
                        if op == '1':
                            get_transactions()
                    case 5:
                        close_program()
            except ValueError:
                print("\n\tOPCION INVALIDA")
    except EOFError:
        close_program()

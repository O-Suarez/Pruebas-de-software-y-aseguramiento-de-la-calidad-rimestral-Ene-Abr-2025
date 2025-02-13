"""
Req 1. Implement a set of classes in Python that
implements two abstractions:
1. Hotel
2. Reservation
3. Customers

Req 2. Implement a set of methods to handle the
next persistent behaviors (stored in files):
1. Hotels
a. Create Hotel
b. Delete Hotel
c. Display Hotel information
d. Modify Hotel Information
e. Reserve a Room
f. Cancel a Reservation

2. Customer
a. Create Customer
b. Delete a Customer
c. Display Customer Information
d. Modify Customer Information

3. Reservation
a. Create a Reservation (Customer,
Hotel)
b. Cancel a Reservation
You are free to decide the attributes within each
class that enable the required behavior.

Req 3. Implement unit test cases to exercise the
methods in each class. Use the unittest module in
Python.

Req 4. The code coverage for all unittests should
accumulate at least 85% of line coverage.

Req 5. The program shall include the mechanism
to handle invalid data in the file. Errors should be
displayed in the console and the execution must
continue.

Req 6. Be compliant with PEP8.

Req 7. The source code must show no warnings
using Fleak and PyLint.
"""
# El nombre del entregable no es aceptado por pylint
# Por eso se desactiva el mensaje C0103
# pylint: disable=C0103
import json
import os
from datetime import datetime
from typing import Dict, Optional


# 1. Hotel
class Hotel:
    """
    Representa un hotel en el sistema, con un ID único, nombre, ubicación,
    y número de habitaciones totales y reservadas.

    Atributos:
        hotel_id (int): ID numérico único para identificar al hotel.
        name (str): Nombre del hotel.
        location (str): Ubicación o ciudad del hotel.
        total_rooms (int): Cantidad total de habitaciones que el hotel posee.
        booked_rooms (int): Cantidad de habitaciones que ya
                            han sido reservadas.

    Métodos estáticos principales:
        create_hotel(name, location, total_rooms): Crea un nuevo hotel y lo
                                                   guarda en el archivo JSON.
        delete_hotel(hotel_id): Elimina un hotel por su ID.
        display_hotel_info(hotel_id): Retorna un objeto Hotel si existe,
                                      o None en caso contrario.
        modify_hotel_information(hotel_id, ...): Modifica la información
                                                 de un hotel existente.
        reserve_room(hotel_id): Reserva una habitación disponible en el hotel.
        cancel_room_reservation(hotel_id): Cancela una reserva existente
                                           (si hay habitaciones ocupadas).
    """
    FILE_PATH = "hotels.json"

    def __init__(self, hotel_id: int, name: str,
                 location: str, total_rooms: int, booked_rooms: int = 0):
        """
        hotel_id: ID entero único
        name: Nombre del hotel
        location: Ciudad o dirección del hotel
        total_rooms: Número total de habitaciones en el hotel
        booked_rooms: Cuántas habitaciones están actualmente reservadas
        """
        self.hotel_id = hotel_id
        self.name = name
        self.location = location
        self.total_rooms = total_rooms
        self.booked_rooms = booked_rooms

    @property
    def available_rooms(self) -> int:
        """
        Cantidad total de habitaciones que el hotel posee.
        """
        return self.total_rooms - self.booked_rooms

    @staticmethod
    def load_hotels() -> Dict[str, dict]:
        """
        Carga todos los hoteles desde el archivo hotels.json
        y los devuelve como un diccionario
        con claves de tipo string (hotel_id).
        """
        if not os.path.exists(Hotel.FILE_PATH):
            return {}
        with open(Hotel.FILE_PATH, 'r', encoding='utf-8') as hotel_file:
            return json.load(hotel_file)

    @staticmethod
    def save_hotels(data: Dict[str, dict]) -> None:
        """
        Guarda el diccionario proporcionado en el archivo hotels.json.
        """
        with open(Hotel.FILE_PATH, 'w', encoding='utf-8') as hotel_file:
            json.dump(data, hotel_file, indent=2)

    # a. Crea un Hotel
    @staticmethod
    def create_hotel(name: str, location: str, total_rooms: int) -> 'Hotel':
        """
        Crea un nuevo Hotel, asigna un nuevo ID,
        lo guarda en JSON y devuelve la instancia de Hotel.
        """
        hotels_data = Hotel.load_hotels()
        # Genera un nuevo ID encontrando el ID máximo existente y añadiéndole 1
        existing_ids = [int(hid) for hid in hotels_data.keys()]
        new_id = max(existing_ids, default=0) + 1

        hotel = Hotel(hotel_id=new_id, name=name,
                      location=location, total_rooms=total_rooms)
        hotels_data[str(new_id)] = {
            "hotel_id": new_id,
            "name": name,
            "location": location,
            "total_rooms": total_rooms,
            "booked_rooms": 0
        }
        Hotel.save_hotels(hotels_data)
        return hotel

    # b. Elimina el Hotel
    @staticmethod
    def delete_hotel(hotel_id: int) -> bool:
        """
        Elimina el hotel con el hotel_id dado del archivo JSON.
        Devuelve True si se eliminó con éxito, o False si el hotel no existe.
        """
        hotels_data = Hotel.load_hotels()
        if str(hotel_id) in hotels_data:
            del hotels_data[str(hotel_id)]
            Hotel.save_hotels(hotels_data)
            return True
        return False

    # c. Muestra la información del Hotel
    @staticmethod
    def display_hotel_info(hotel_id: int) -> Optional['Hotel']:
        """
        Devuelve una instancia de Hotel para el hotel_id dado,
        o None si no existe.
        """
        hotels_data = Hotel.load_hotels()
        data = hotels_data.get(str(hotel_id))
        print(data)
        if data is None:
            return None
        return Hotel(**data)

    # d. Modifica la información del Hotel
    @staticmethod
    def modify_hotel_information(hotel_id: int, name: str = None,
                                 location: str = None,
                                 total_rooms: int = None) -> bool:
        """
        Modifica la información del hotel si existe.
        Devuelve True si se modificó con éxito, False en caso contrario.
        """
        hotels_data = Hotel.load_hotels()
        hotel_dict = hotels_data.get(str(hotel_id))
        if not hotel_dict:
            return False

        if name is not None:
            hotel_dict["name"] = name
        if location is not None:
            hotel_dict["location"] = location
        if total_rooms is not None:
            # Nos aseguramos de que el nuevo total
            # no sea menor que las habitaciones ya reservadas
            if total_rooms < hotel_dict["booked_rooms"]:
                return False
            hotel_dict["total_rooms"] = total_rooms

        hotels_data[str(hotel_id)] = hotel_dict
        Hotel.save_hotels(hotels_data)
        return True

    # e. Reserva una habitación
    @staticmethod
    def reserve_room(hotel_id: int) -> bool:
        """
        Reserva una sola habitación en el hotel especificado.
        Devuelve True si se reservó con éxito, False en caso contrario.
        """
        hotels_data = Hotel.load_hotels()
        hotel_dict = hotels_data.get(str(hotel_id))
        if not hotel_dict:
            return False

        available_rooms = (hotel_dict["total_rooms"]
                           - hotel_dict["booked_rooms"])
        if available_rooms > 0:
            hotel_dict["booked_rooms"] += 1
            hotels_data[str(hotel_id)] = hotel_dict
            Hotel.save_hotels(hotels_data)
            return True
        return False

    # f. Cancela una Reservacion
    @staticmethod
    def cancel_room_reservation(hotel_id: int) -> bool:
        """
        Cancela (libera) una sola habitación reservada
        en el hotel especificado, si es posible.
        Devuelve True si se liberó con éxito, o False en caso contrario.
        """
        hotels_data = Hotel.load_hotels()
        hotel_dict = hotels_data.get(str(hotel_id))
        if not hotel_dict:
            return False

        if hotel_dict["booked_rooms"] > 0:
            hotel_dict["booked_rooms"] -= 1
            hotels_data[str(hotel_id)] = hotel_dict
            Hotel.save_hotels(hotels_data)
            return True
        return False

    def __repr__(self):
        return (f"Hotel(hotel_id={self.hotel_id}, name='{self.name}', "
                f"location='{self.location}', total_rooms={self.total_rooms}, "
                f"booked_rooms={self.booked_rooms})")


# 2. Cliente
class Customer:
    """
    Representa un cliente que puede realizar reservas de hotel.

    Atributos:
        customer_id (int): ID numérico único para identificar al cliente.
        name (str): Nombre del cliente.
        email (str): Correo electrónico del cliente.

    Métodos estáticos principales:
        create_customer(name, email): Crea un nuevo cliente
                                      y lo guarda en el archivo JSON.
        delete_customer(customer_id): Elimina un cliente por su ID.
        display_customer_info(customer_id): Retorna un objeto Customer si
                                            existe, o None en caso contrario.
        modify_customer_information(customer_id, ...): Modifica los datos de
                                                       un cliente existente.
    """
    FILE_PATH = "customers.json"

    def __init__(self, customer_id: int, name: str, email: str):
        self.customer_id = customer_id
        self.name = name
        self.email = email

    @staticmethod
    def load_customers() -> Dict[str, dict]:
        """
        Carga todos los clientes desde el archivo customers.json
        y los devuelve como un diccionario
        con claves de tipo string (hotel_id).
        """
        if not os.path.exists(Customer.FILE_PATH):
            return {}
        with open(Customer.FILE_PATH, 'r', encoding='utf-8') as customer_file:
            return json.load(customer_file)

    @staticmethod
    def save_customers(data: Dict[str, dict]) -> None:
        """
        Guarda el diccionario proporcionado en el archivo customers.json.
        """
        with open(Customer.FILE_PATH, 'w', encoding='utf-8') as customer_file:
            json.dump(data, customer_file, indent=2)

    # a. Crea un Cliente
    @staticmethod
    def create_customer(name: str, email: str) -> 'Customer':
        """
        Crea un nuevo cliente, asigna un nuevo ID,
        lo guarda en JSON y devuelve la instancia de cliente.
        """
        customers_data = Customer.load_customers()
        existing_ids = [int(cid) for cid in customers_data.keys()]
        new_id = max(existing_ids, default=0) + 1

        cust = Customer(customer_id=new_id, name=name, email=email)
        customers_data[str(new_id)] = {
            "customer_id": new_id,
            "name": name,
            "email": email
        }
        Customer.save_customers(customers_data)
        return cust

    # b. Elimina un Cliente
    @staticmethod
    def delete_customer(customer_id: int) -> bool:
        """
        Elimina el cliente con el customer_id dado del archivo JSON.
        Devuelve True si se eliminó con éxito, o False si el cliente no existe.
        """
        customers_data = Customer.load_customers()
        if str(customer_id) in customers_data:
            del customers_data[str(customer_id)]
            Customer.save_customers(customers_data)
            return True
        return False

    # c. Muestra la Información de un Cliente
    @staticmethod
    def display_customer_info(customer_id: int
                              ) -> Optional['Customer']:
        """
        Devuelve una instancia de cliente para el customer_id dado,
        o None si no existe.
        """
        customers_data = Customer.load_customers()
        data = customers_data.get(str(customer_id))
        print(data)
        if data is None:
            return None
        return Customer(**data)

    # d. Modifica la Información de un Cliente
    @staticmethod
    def modify_customer_information(customer_id: int, name: str = None,
                                    email: str = None) -> bool:
        """
        Modifica la información un cliente si existe.
        Devuelve True si se modificó con éxito, False en caso contrario.
        """
        customers_data = Customer.load_customers()
        cust_dict = customers_data.get(str(customer_id))
        if not cust_dict:
            return False

        if name is not None:
            cust_dict["name"] = name
        if email is not None:
            cust_dict["email"] = email

        customers_data[str(customer_id)] = cust_dict
        Customer.save_customers(customers_data)
        return True

    def __repr__(self):
        return (f"Customer(customer_id={self.customer_id}, "
                f"name='{self.name}', email='{self.email}')")


# 3. Reservacion
class Reservation:
    """
    Representa una reserva realizada por un cliente en un hotel.

    Atributos:
        reservation_id (int): ID numérico único de la reserva.
        customer_id (int): ID del cliente que realizó la reserva.
        hotel_id (int): ID del hotel en el que se realizó la reserva.
        check_in (str): Fecha de entrada en formato 'YYYY-MM-DD'.
        check_out (str): Fecha de salida en formato 'YYYY-MM-DD'.
        is_active (bool): Indica si la reservacion está activa o cancelada.

    Métodos estáticos principales:
        create_reservation(customer_id, hotel_id, check_in, check_out):
            Crea una nueva reservacion si el cliente
            y el hotel existen y hay habitaciones disponibles.
        cancel_reservation(reservation_id): Cancela una reserva activa
                                            y libera la habitación en el hotel.
    """
    FILE_PATH = "reservations.json"

    def __init__(self, reservation_id: int, customer_id: int, hotel_id: int,
                 check_in: str, check_out: str, is_active: bool = True):
        """
        reservation_id: ID entero único
        customer_id: El ID del cliente que hace la reservacion
        hotel_id: El ID del hotel que se reservacion
        check_in: Fecha de entrada como string (por ejemplo "2025-03-01")
        check_out: Fecha de salida como string (por ejemplo "2025-03-05")
        is_active: Booleano que indica si la Reservacion está activa
        """
        self.reservation_id = reservation_id
        self.customer_id = customer_id
        self.hotel_id = hotel_id
        self.check_in = check_in
        self.check_out = check_out
        self.is_active = is_active

    @staticmethod
    def load_reservations() -> Dict[str, dict]:
        """
        Carga todas las reservaciones desde el archivo reservations.json
        y los devuelve como un diccionario.
        """
        if not os.path.exists(Reservation.FILE_PATH):
            return {}
        with open(Reservation.FILE_PATH, 'r', encoding='utf-8') as res_file:
            return json.load(res_file)

    @staticmethod
    def save_reservations(data: Dict[str, dict]) -> None:
        """
        Guarda el diccionario proporcionado en el archivo reservations.json.
        """
        with open(Reservation.FILE_PATH, 'w', encoding='utf-8') as res_file:
            json.dump(data, res_file, indent=2)

    # a. Crea una Reservacion (Cliente, Hotel)
    @staticmethod
    def create_reservation(customer_id: int, hotel_id: int, check_in: datetime,
                           check_out: datetime) -> Optional['Reservation']:
        """
        Crea una nueva reservacion si el cliente y el hotel existen
        y si hay una habitación disponible.
        Devuelve el objeto reservation si tiene éxito, o None si falla.
        """
        # 1. Verifica que el cliente y el hotel existan
        customer = Customer.display_customer_info(customer_id)
        hotel = Hotel.display_hotel_info(hotel_id)
        if not customer or not hotel:
            print("Error: Cliente o hotel inválido.")
            return None

        # 2. Intenta reservar una habitación en el hotel
        if not Hotel.reserve_room(hotel_id):
            print("Error: No hay habitaciones disponibles.")
            return None

        # 3. Crea el registro de la reservacion
        reservations_data = Reservation.load_reservations()
        existing_ids = [int(rid) for rid in reservations_data.keys()]
        new_id = max(existing_ids, default=0) + 1

        # Almacena las fechas como strings para JSON
        check_in_str = check_in.strftime("%Y-%m-%d")
        check_out_str = check_out.strftime("%Y-%m-%d")

        reservation = Reservation(
            reservation_id=new_id,
            customer_id=customer_id,
            hotel_id=hotel_id,
            check_in=check_in_str,
            check_out=check_out_str,
            is_active=True
        )
        reservations_data[str(new_id)] = {
            "reservation_id": new_id,
            "customer_id": customer_id,
            "hotel_id": hotel_id,
            "check_in": check_in_str,
            "check_out": check_out_str,
            "is_active": True
        }
        Reservation.save_reservations(reservations_data)
        return reservation

    # b. Cancelar una reservacion
    @staticmethod
    def cancel_reservation(reservation_id: int) -> bool:
        """
        Cancela una reservacion existente (la marca como inactiva)
        y libera una habitación en el hotel.
        Devuelve True si tuvo éxito, False en caso contrario.
        """
        reservations_data = Reservation.load_reservations()
        res_dict = reservations_data.get(str(reservation_id))
        if not res_dict:
            return False
        if not res_dict["is_active"]:
            # Ya estaba cancelada
            return False

        # Marca la reservacion como inactiva
        res_dict["is_active"] = False
        reservations_data[str(reservation_id)] = res_dict
        Reservation.save_reservations(reservations_data)

        # Libera la habitación en el hotel
        hotel_id = res_dict["hotel_id"]
        Hotel.cancel_room_reservation(hotel_id)
        return True

    def __repr__(self):
        return (
            f"Reservation("
            f"reservation_id={self.reservation_id}, "
            f"customer_id={self.customer_id}, "
            f"hotel_id={self.hotel_id}, "
            f"check_in='{self.check_in}', "
            f"check_out='{self.check_out}', "
            f"is_active={self.is_active})")


# Función principal
def main():
    """
    Función principal que crea y manipula hoteles, clientes y reservas.
    """
    # Nos aseguramos de que existan los archivos JSON (con diccionarios vacíos)
    for filename in ["hotels.json", "customers.json", "reservations.json"]:
        if not os.path.exists(filename):
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({}, f)

    # 1. Crea un Hotel
    mi_hotel = Hotel.create_hotel("Grand Plaza", "New York", total_rooms=10)
    print("Hotel creado:", mi_hotel)

    # 2. Muestra la información del Hotel
    hotel_obtenido = Hotel.display_hotel_info(mi_hotel.hotel_id)
    print("Información del Hotel:", hotel_obtenido)

    # 3. Crea un Cliente
    mi_cliente = Customer.create_customer("John Doe", "john@example.com")
    print("Cliente creado:", mi_cliente)

    # 4. Crea una Reservación
    fecha_entrada = datetime(2025, 3, 1)
    fecha_salida = datetime(2025, 3, 5)
    mi_reserva = Reservation.create_reservation(
        customer_id=mi_cliente.customer_id,
        hotel_id=mi_hotel.hotel_id,
        check_in=fecha_entrada,
        check_out=fecha_salida
    )
    print("Reserva creada:", mi_reserva)

    # 5. Cancela la Reservación
    if mi_reserva:
        exito_cancelar = Reservation.cancel_reservation(
                         mi_reserva.reservation_id)
        print("Reserva cancelada:", exito_cancelar)

    # 6. Modifica el Hotel
    Hotel.modify_hotel_information(
        mi_hotel.hotel_id,
        name="Grand Plaza - Renovado",
        total_rooms=12
    )
    hotel_modificado = Hotel.display_hotel_info(mi_hotel.hotel_id)
    print("Hotel modificado:", hotel_modificado)

    # 7. Elimina el Hotel
    exito_eliminar_hotel = Hotel.delete_hotel(mi_hotel.hotel_id)
    print("Hotel eliminado:", exito_eliminar_hotel)

    # 8. Elimina el Cliente
    exito_eliminar_cliente = Customer.delete_customer(mi_cliente.customer_id)
    print("Cliente eliminado:", exito_eliminar_cliente)


if __name__ == "__main__":
    main()

"""
Este módulo contiene las pruebas unitarias para las clases Hotel, Customer y
Reservation. Utiliza unittest para realizar las verificaciones y crea archivos
JSON temporales para garantizar un entorno limpio en cada prueba.
"""

import unittest
import tempfile
import os
import json
from datetime import datetime


from A01323987_A6_2 import Hotel, Customer, Reservation


class TestHotel(unittest.TestCase):
    """
    Contiene pruebas unitarias para la clase Hotel: creación, eliminación,
    modificación, reserva y cancela habitaciones.
    """

    def setUp(self):
        """
        Crea un archivo JSON temporal para hoteles,
        reemplaza la ruta Hotel.FILE_PATH
        para usarlo y así aislar cada prueba.
        """
        self.temp_hotel_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".json"
        )
        self.temp_hotel_file.close()

        # Nos aseguramos que el archivo comience vacío
        with open(self.temp_hotel_file.name,
                  'w', encoding='utf-8') as file_obj:
            json.dump({}, file_obj)

        self.old_hotel_file = Hotel.FILE_PATH
        Hotel.FILE_PATH = self.temp_hotel_file.name

    def tearDown(self):
        """
        Elimina el archivo temporal creado en setUp
        y restablece la ruta original.
        """
        os.remove(self.temp_hotel_file.name)
        Hotel.FILE_PATH = self.old_hotel_file

    def test_create_hotel(self):
        """
        Prueba la creación de un hotel y verifica sus atributos por defecto.
        """
        hotel = Hotel.create_hotel(
            name="Hotel de Prueba",
            location="Ciudad de Prueba",
            total_rooms=5
        )
        self.assertIsNotNone(
            hotel,
            "La creación debe retornar un objeto Hotel."
        )
        self.assertEqual(hotel.name, "Hotel de Prueba")
        self.assertEqual(hotel.location, "Ciudad de Prueba")
        self.assertEqual(hotel.total_rooms, 5)
        self.assertEqual(hotel.booked_rooms, 0)

    def test_display_hotel_info(self):
        """
        Prueba la función de mostrar información para un hotel recién creado.
        """
        hotel = Hotel.create_hotel(
            "Hotel para Mostrar",
            "Ciudad Muestra",
            10
        )
        fetched = Hotel.display_hotel_info(hotel.hotel_id)
        self.assertIsNotNone(
            fetched,
            "Debe poder obtenerse el hotel recién creado."
        )
        self.assertEqual(fetched.hotel_id, hotel.hotel_id)
        self.assertEqual(fetched.name, "Hotel para Mostrar")

    def test_modify_hotel_information(self):
        """
        Prueba la modificación de la información de un hotel existente.
        """
        hotel = Hotel.create_hotel(
            "Nombre Viejo",
            "Ciudad Vieja",
            10
        )
        success = Hotel.modify_hotel_information(
            hotel_id=hotel.hotel_id,
            name="Nombre Nuevo",
            location="Ciudad Nueva",
            total_rooms=12
        )
        self.assertTrue(
            success,
            "La modificación debe ser exitosa con datos válidos."
        )
        updated = Hotel.display_hotel_info(hotel.hotel_id)
        self.assertEqual(updated.name, "Nombre Nuevo")
        self.assertEqual(updated.location, "Ciudad Nueva")
        self.assertEqual(updated.total_rooms, 12)

    def test_delete_hotel(self):
        """
        Prueba la eliminación de un hotel
        y verifica que no exista posteriormente.
        """
        hotel = Hotel.create_hotel(
            "Hotel a Eliminar",
            "Ciudad Eliminada",
            5
        )
        deleted = Hotel.delete_hotel(hotel.hotel_id)
        self.assertTrue(
            deleted,
            "El hotel debe poder eliminarse correctamente."
        )
        self.assertIsNone(
            Hotel.display_hotel_info(hotel.hotel_id),
            "El hotel ya no debe existir."
        )

    def test_reserve_room(self):
        """
        Prueba la acción de reservar habitaciones
        en un hotel con capacidad limitada.
        """
        hotel = Hotel.create_hotel(
            "Hotel Reserva",
            "Ciudad Reserva",
            2
        )
        self.assertTrue(
            Hotel.reserve_room(hotel.hotel_id),
            "Debe poder reservar la primera habitación."
        )
        self.assertTrue(
            Hotel.reserve_room(hotel.hotel_id),
            "Debe poder reservar la segunda habitación."
        )
        # No hay más habitaciones disponibles
        self.assertFalse(
            Hotel.reserve_room(hotel.hotel_id),
            "No debe reservar más allá de la capacidad."
        )

    def test_cancel_room_reservation(self):
        """
        Prueba la cancelación de una habitación reservada.
        """
        hotel = Hotel.create_hotel(
            "Hotel Cancelación",
            "Ciudad Cancelación",
            2
        )
        # Reservar 2 habitaciones
        Hotel.reserve_room(hotel.hotel_id)
        Hotel.reserve_room(hotel.hotel_id)
        # Cancelar 1 reservación
        canceled = Hotel.cancel_room_reservation(hotel.hotel_id)
        self.assertTrue(
            canceled,
            "Se debe poder cancelar una reservación de habitación."
        )
        fetched = Hotel.display_hotel_info(hotel.hotel_id)
        self.assertEqual(
            fetched.booked_rooms,
            1,
            "Las habitaciones reservadas deben reducirse en 1."
        )


class TestCustomer(unittest.TestCase):
    """
    Contiene pruebas unitarias para la clase Customer: creación, modificación,
    eliminación y visualización de clientes.
    """

    def setUp(self):
        """
        Crea un archivo JSON temporal para clientes
        y reemplaza Customer.FILE_PATH
        para aislar cada prueba.
        """
        self.temp_customer_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".json"
        )
        self.temp_customer_file.close()
        with open(self.temp_customer_file.name,
                  'w', encoding='utf-8') as file_obj:
            json.dump({}, file_obj)

        self.old_customer_file = Customer.FILE_PATH
        Customer.FILE_PATH = self.temp_customer_file.name

    def tearDown(self):
        """
        Elimina el archivo temporal y restablece la ruta original del archivo
        de clientes.
        """
        os.remove(self.temp_customer_file.name)
        Customer.FILE_PATH = self.old_customer_file

    def test_create_customer(self):
        """
        Prueba la creación de un cliente y verifica sus atributos.
        """
        customer = Customer.create_customer("Jane Doe", "jane@example.com")
        self.assertIsNotNone(
            customer,
            "Debe retornar un objeto Customer."
        )
        self.assertEqual(customer.name, "Jane Doe")

    def test_display_customer_info(self):
        """
        Prueba la obtención de la información de un cliente recién creado.
        """
        customer = Customer.create_customer("John", "john@example.com")
        fetched = Customer.display_customer_info(customer.customer_id)
        self.assertIsNotNone(
            fetched,
            "Debe poder obtenerse el cliente creado."
        )
        self.assertEqual(fetched.email, "john@example.com")

    def test_modify_customer_information(self):
        """
        Prueba la modificación de la información de un cliente.
        """
        customer = Customer.create_customer(
            "NombreViejo",
            "viejo@correo.com"
        )
        success = Customer.modify_customer_information(
            customer_id=customer.customer_id,
            name="NombreNuevo",
            email="nuevo@correo.com"
        )
        self.assertTrue(
            success,
            "La modificación debe ser exitosa."
        )
        updated = Customer.display_customer_info(customer.customer_id)
        self.assertEqual(updated.name, "NombreNuevo")
        self.assertEqual(updated.email, "nuevo@correo.com")

    def test_delete_customer(self):
        """
        Prueba la eliminación de un cliente y verifica que no exista luego.
        """
        customer = Customer.create_customer("Borrar Este", "borrar@correo.com")
        deleted = Customer.delete_customer(customer.customer_id)
        self.assertTrue(
            deleted,
            "El cliente debe eliminarse correctamente."
        )
        self.assertIsNone(
            Customer.display_customer_info(customer.customer_id),
            "El cliente no debe existir más."
        )


class TestReservation(unittest.TestCase):
    """
    Contiene pruebas unitarias para la clase Reservation: crea y cancela
    reservaciones, validando la disponibilidad en el hotel y la asociación con
    el cliente.
    """

    def setUp(self):
        """
        Crea archivos JSON temporales para hoteles, clientes y reservaciones,
        luego modifica las rutas de cada clase (FILE_PATH)
        para aislar cada prueba.
        """
        self.temp_hotel_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".json"
        )
        self.temp_hotel_file.close()
        with open(self.temp_hotel_file.name,
                  'w', encoding='utf-8') as file_obj:
            json.dump({}, file_obj)

        self.temp_customer_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".json"
        )
        self.temp_customer_file.close()
        with open(self.temp_customer_file.name,
                  'w', encoding='utf-8') as file_obj:
            json.dump({}, file_obj)

        self.temp_reservation_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".json"
        )
        self.temp_reservation_file.close()
        with open(self.temp_reservation_file.name,
                  'w', encoding='utf-8') as file_obj:
            json.dump({}, file_obj)

        self.old_hotel_file = Hotel.FILE_PATH
        Hotel.FILE_PATH = self.temp_hotel_file.name

        self.old_customer_file = Customer.FILE_PATH
        Customer.FILE_PATH = self.temp_customer_file.name

        self.old_reservation_file = Reservation.FILE_PATH
        Reservation.FILE_PATH = self.temp_reservation_file.name

    def tearDown(self):
        """
        Elimina los archivos temporales y restablece los paths originales de
        Hotel, Customer y Reservation.
        """
        os.remove(self.temp_hotel_file.name)
        os.remove(self.temp_customer_file.name)
        os.remove(self.temp_reservation_file.name)

        Hotel.FILE_PATH = self.old_hotel_file
        Customer.FILE_PATH = self.old_customer_file
        Reservation.FILE_PATH = self.old_reservation_file

    def test_create_reservation(self):
        """
        Prueba la creación de una reservación válida y verifica que el hotel
        tenga una habitación ocupada.
        """
        hotel = Hotel.create_hotel("ResTest Hotel", "ResTest City", 2)
        customer = Customer.create_customer("ResTest User",
                                            "resuser@example.com")

        check_in = datetime(2025, 3, 1)
        check_out = datetime(2025, 3, 5)
        reservacion = Reservation.create_reservation(
            customer_id=customer.customer_id,
            hotel_id=hotel.hotel_id,
            check_in=check_in,
            check_out=check_out
        )
        self.assertIsNotNone(
            reservacion,
            "Se debe poder crear la reservación correctamente."
        )
        self.assertTrue(
            reservacion.is_active,
            "La reservación debe estar activa."
        )
        updated_hotel = Hotel.display_hotel_info(hotel.hotel_id)
        self.assertEqual(updated_hotel.booked_rooms, 1)

    def test_create_reservation_invalid_hotel(self):
        """
        Prueba la creación de una reservación con un hotel inexistente.
        Se espera un error impreso y un return de None.
        """
        print(
            "::: Se espera un mensaje de error a continuación, "
            "debido a un hotel inexistente :::"
        )
        customer = Customer.create_customer("SinHotel User",
                                            "nohotel@example.com")
        reservacion = Reservation.create_reservation(
            customer_id=customer.customer_id,
            hotel_id=9999,  # No existe
            check_in=datetime(2025, 3, 1),
            check_out=datetime(2025, 3, 5)
        )
        self.assertIsNone(
            reservacion,
            "Debe fallar si el hotel no existe."
        )

    def test_create_reservation_invalid_customer(self):
        """
        Prueba la creación de una reservación con un cliente inexistente.
        Se espera un error impreso y un return de None.
        """
        print(
            "::: Se espera un mensaje de error a continuación, "
            "debido a un cliente inexistente :::"
        )
        hotel = Hotel.create_hotel("Solo Hotel", "Ciudad Sola", 1)
        reservacion = Reservation.create_reservation(
            customer_id=9999,  # No existe
            hotel_id=hotel.hotel_id,
            check_in=datetime(2025, 3, 1),
            check_out=datetime(2025, 3, 5)
        )
        self.assertIsNone(
            reservacion,
            "Debe fallar si el cliente no existe."
        )

    def test_create_reservation_no_rooms_available(self):
        """
        Prueba la creación de reservaciones en un hotel con solo 1 habitación.
        La segunda reservación debe fallar.
        """
        print(
            "::: Se espera un mensaje de error a continuación, "
            "por falta de habitaciones :::"
        )
        hotel = Hotel.create_hotel("Pequeño Hotel",
                                   "Mini Ciudad",
                                   total_rooms=1)
        customer = Customer.create_customer("Usuario Uno", "uno@example.com")

        # Primera reservación con éxito
        res1 = Reservation.create_reservation(
            customer_id=customer.customer_id,
            hotel_id=hotel.hotel_id,
            check_in=datetime(2025, 3, 1),
            check_out=datetime(2025, 3, 2)
        )
        self.assertIsNotNone(
            res1,
            "La primera reservación debe realizarse con éxito."
        )

        # Segunda reservación debe fallar
        res2 = Reservation.create_reservation(
            customer_id=customer.customer_id,
            hotel_id=hotel.hotel_id,
            check_in=datetime(2025, 3, 2),
            check_out=datetime(2025, 3, 3)
        )
        self.assertIsNone(
            res2,
            "No hay habitaciones disponibles para una segunda reservación."
        )

    def test_cancel_reservation(self):
        """
        Prueba la cancelación de una reservación activa,
        verificando que se libere
        la habitación del hotel.
        """
        hotel = Hotel.create_hotel("CancelarRes Hotel", "CancelarRes City", 1)
        customer = Customer.create_customer(
            "CancelarRes User",
            "cancelres@example.com"
        )
        check_in = datetime(2025, 4, 1)
        check_out = datetime(2025, 4, 5)
        reservacion = Reservation.create_reservation(
            customer_id=customer.customer_id,
            hotel_id=hotel.hotel_id,
            check_in=check_in,
            check_out=check_out
        )
        self.assertIsNotNone(
            reservacion,
            "Se debe crear la reservación."
        )
        self.assertTrue(
            reservacion.is_active,
            "La reservación debe inicializarse como activa."
        )

        canceled = Reservation.cancel_reservation(reservacion.reservation_id)
        self.assertTrue(canceled, "La cancelación debe ser exitosa.")
        reservations_data = Reservation.load_reservations()
        res_info = reservations_data[str(reservacion.reservation_id)]
        self.assertFalse(
            res_info["is_active"],
            "La reservación ahora debe ser inactiva."
        )
        updated_hotel = Hotel.display_hotel_info(hotel.hotel_id)
        self.assertEqual(updated_hotel.booked_rooms, 0)


def main():
    """
    Función principal que carga y ejecuta todas las pruebas, mostrando
    cuántas fueron exitosas de cuántas totales.
    """
    suite = unittest.defaultTestLoader.loadTestsFromModule(
            __import__(__name__))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    total_tests = result.testsRun
    failed_tests = len(result.failures)
    errored_tests = len(result.errors)
    successful_tests = total_tests - failed_tests - errored_tests

    print("\n" + "-" * 74)
    print(f"PRUEBAS EXITOSAS: {successful_tests} de {total_tests}")
    print("-" * 74 + "\n")


if __name__ == "__main__":
    main()

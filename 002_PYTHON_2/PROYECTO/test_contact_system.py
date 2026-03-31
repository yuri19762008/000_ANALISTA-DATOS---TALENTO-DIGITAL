"""Pruebas unitarias para Contact y ContactManager"""

import unittest
import os
from contact import Contact
from contact_manager import ContactManager


class TestContact(unittest.TestCase):
    def setUp(self):
        self.contacto = Contact(
            "Juan García",
            "+56912345678",
            "juan@example.com",
            "Calle Principal 123",
        )

    def test_crear_contacto(self):
        self.assertEqual(self.contacto.nombre, "Juan García")
        self.assertEqual(self.contacto.telefono, "+56912345678")
        self.assertEqual(self.contacto.email, "juan@example.com")
        self.assertEqual(self.contacto.direccion, "Calle Principal 123")

    def test_actualizar_nombre(self):
        self.contacto.nombre = "María García"
        self.assertEqual(self.contacto.nombre, "María García")

    def test_actualizar_email(self):
        self.contacto.email = "maria@example.com"
        self.assertEqual(self.contacto.email, "maria@example.com")

    def test_actualizar_direccion(self):
        self.contacto.direccion = "Calle Secundaria 456"
        self.assertEqual(self.contacto.direccion, "Calle Secundaria 456")

    def test_nombre_vacio_invalido(self):
        with self.assertRaises(ValueError):
            self.contacto.nombre = ""

    def test_email_vacio_invalido(self):
        with self.assertRaises(ValueError):
            self.contacto.email = ""

    def test_direccion_vacia_invalida(self):
        with self.assertRaises(ValueError):
            self.contacto.direccion = ""

    def test_to_dict(self):
        d = self.contacto.to_dict()
        self.assertEqual(d["nombre"], "Juan García")
        self.assertEqual(d["telefono"], "+56912345678")

    def test_from_dict(self):
        datos = {
            "nombre": "Pedro López",
            "telefono": "+56987654321",
            "email": "pedro@example.com",
            "direccion": "Avenida Central 789",
        }
        c = Contact.from_dict(datos)
        self.assertEqual(c.nombre, "Pedro López")
        self.assertEqual(c.telefono, "+56987654321")

    def test_str_representation(self):
        s = str(self.contacto)
        self.assertIn("Juan García", s)
        self.assertIn("+56912345678", s)


class TestContactManager(unittest.TestCase):
    def setUp(self):
        self.archivo_pruebas = "test_contactos.json"
        if os.path.exists(self.archivo_pruebas):
            os.remove(self.archivo_pruebas)
        self.gestor = ContactManager(self.archivo_pruebas)

    def tearDown(self):
        if os.path.exists(self.archivo_pruebas):
            os.remove(self.archivo_pruebas)

    def test_agregar_contacto(self):
        self.gestor.agregar_contacto(
            "Ana Silva",
            "+56912345678",
            "ana@example.com",
            "Paseo del Mar 101",
        )
        self.assertEqual(self.gestor.obtener_cantidad_contactos(), 1)

    def test_agregar_contacto_telefono_duplicado(self):
        self.gestor.agregar_contacto(
            "Ana Silva",
            "+56912345678",
            "ana@example.com",
            "Paseo del Mar 101",
        )
        with self.assertRaises(ValueError):
            self.gestor.agregar_contacto(
                "Otro Nombre",
                "+56912345678",
                "otro@example.com",
                "Otra Dirección",
            )

    def test_buscar_por_nombre(self):
        self.gestor.agregar_contacto(
            "Carlos Ruiz",
            "+56912345678",
            "carlos@example.com",
            "Calle de la Paz 202",
        )
        resultados = self.gestor.buscar_por_nombre("Carlos")
        self.assertEqual(len(resultados), 1)
        self.assertEqual(resultados[0].nombre, "Carlos Ruiz")

    def test_buscar_por_nombre_sin_resultados(self):
        self.gestor.agregar_contacto(
            "Carlos Ruiz",
            "+56912345678",
            "carlos@example.com",
            "Calle de la Paz 202",
        )
        resultados = self.gestor.buscar_por_nombre("Inexistente")
        self.assertEqual(len(resultados), 0)

    def test_buscar_por_telefono(self):
        self.gestor.agregar_contacto(
            "Diana Santos",
            "+56987654321",
            "diana@example.com",
            "Avenida del Río 303",
        )
        contacto = self.gestor.buscar_por_telefono("+56987654321")
        self.assertIsNotNone(contacto)
        self.assertEqual(contacto.nombre, "Diana Santos")

    def test_buscar_por_telefono_no_existe(self):
        contacto = self.gestor.buscar_por_telefono("+56912345678")
        self.assertIsNone(contacto)

    def test_editar_contacto(self):
        self.gestor.agregar_contacto(
            "Eduardo López",
            "+56912345678",
            "eduardo@example.com",
            "Boulevard Central 404",
        )
        self.gestor.editar_contacto(
            "+56912345678",
            nombre="Eduardo Martínez",
            email="enew@example.com",
        )
        contacto = self.gestor.buscar_por_telefono("+56912345678")
        self.assertEqual(contacto.nombre, "Eduardo Martínez")
        self.assertEqual(contacto.email, "enew@example.com")

    def test_editar_contacto_inexistente(self):
        with self.assertRaises(ValueError):
            self.gestor.editar_contacto("+56999999999", nombre="Nuevo Nombre")

    def test_eliminar_contacto(self):
        self.gestor.agregar_contacto(
            "Fátima Núñez",
            "+56912345678",
            "fatima@example.com",
            "Pasaje del Bosque 505",
        )
        self.assertEqual(self.gestor.obtener_cantidad_contactos(), 1)
        self.gestor.eliminar_contacto("+56912345678")
        self.assertEqual(self.gestor.obtener_cantidad_contactos(), 0)

    def test_eliminar_contacto_inexistente(self):
        with self.assertRaises(ValueError):
            self.gestor.eliminar_contacto("+56999999999")

    def test_obtener_todos_contactos(self):
        self.gestor.agregar_contacto(
            "Contacto 1",
            "+56911111111",
            "contacto1@example.com",
            "Dirección 1",
        )
        self.gestor.agregar_contacto(
            "Contacto 2",
            "+56922222222",
            "contacto2@example.com",
            "Dirección 2",
        )
        contactos = self.gestor.obtener_todos_contactos()
        self.assertEqual(len(contactos), 2)

    def test_persistencia_datos(self):
        self.gestor.agregar_contacto(
            "Persistencia Test",
            "+56912345678",
            "test@example.com",
            "Test Address",
        )
        gestor2 = ContactManager(self.archivo_pruebas)
        contactos = gestor2.obtener_todos_contactos()
        self.assertEqual(len(contactos), 1)
        self.assertEqual(contactos[0].nombre, "Persistencia Test")


if __name__ == "__main__":
    unittest.main(verbosity=2)

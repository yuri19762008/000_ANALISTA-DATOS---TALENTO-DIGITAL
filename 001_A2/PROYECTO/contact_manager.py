"""Módulo ContactManager - Gestor de contactos con almacenamiento en JSON"""

import json
import os
from contact import Contact


class ContactManager:
    """
    Gestor de contactos.

    Responsabilidades:
    - Agregar, editar y eliminar contactos
    - Buscar contactos por nombre o teléfono
    - Persistencia de datos en JSON
    - Gestión de la lista de contactos
    """

    def __init__(self, archivo_datos: str = "contactos.json"):
        self._archivo_datos = archivo_datos
        self._contactos: list[Contact] = []
        self._cargar_contactos()

    def _cargar_contactos(self):
        """Carga los contactos desde el archivo JSON"""
        if os.path.exists(self._archivo_datos):
            try:
                with open(self._archivo_datos, "r", encoding="utf-8") as archivo:
                    datos = json.load(archivo)
                    self._contactos = [Contact.from_dict(c) for c in datos]
                print(f"✅ {len(self._contactos)} contactos cargados correctamente")
            except Exception as e:
                print(f"⚠️  Error al cargar contactos: {e}")
                self._contactos = []
        else:
            self._contactos = []

    def _guardar_contactos(self):
        """Guarda los contactos en el archivo JSON"""
        try:
            datos = [c.to_dict() for c in self._contactos]
            with open(self._archivo_datos, "w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, indent=2, ensure_ascii=False)
        except Exception as e:
            raise Exception(f"Error al guardar contactos: {e}")

    def agregar_contacto(self, nombre: str, telefono: str, email: str, direccion: str):
        """Agrega un nuevo contacto"""
        if self.buscar_por_telefono(telefono):
            raise ValueError(f"Ya existe un contacto con el teléfono '{telefono}'")

        nuevo_contacto = Contact(nombre, telefono, email, direccion)
        self._contactos.append(nuevo_contacto)
        self._guardar_contactos()

    def editar_contacto(self, telefono: str, nombre: str = None, email: str = None, direccion: str = None):
        """Edita un contacto existente"""
        contacto = self.buscar_por_telefono(telefono)
        if not contacto:
            raise ValueError(f"No existe contacto con el teléfono '{telefono}'")

        if nombre:
            contacto.nombre = nombre
        if email:
            contacto.email = email
        if direccion:
            contacto.direccion = direccion

        self._guardar_contactos()

    def eliminar_contacto(self, telefono: str):
        """Elimina un contacto"""
        contacto = self.buscar_por_telefono(telefono)
        if not contacto:
            raise ValueError(f"No existe contacto con el teléfono '{telefono}'")

        self._contactos.remove(contacto)
        self._guardar_contactos()

    def buscar_por_nombre(self, nombre: str) -> list[Contact]:
        """Busca contactos por nombre (búsqueda parcial)"""
        nombre_busqueda = nombre.lower()
        return [c for c in self._contactos if nombre_busqueda in c.nombre.lower()]

    def buscar_por_telefono(self, telefono: str) -> Contact | None:
        """Busca un contacto por teléfono (búsqueda exacta)"""
        for contacto in self._contactos:
            if contacto.telefono == telefono:
                return contacto
        return None

    def obtener_todos_contactos(self) -> list[Contact]:
        """Obtiene todos los contactos"""
        return self._contactos

    def obtener_cantidad_contactos(self) -> int:
        """Obtiene la cantidad total de contactos"""
        return len(self._contactos)

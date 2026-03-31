"""Módulo Contacto - Clase Contact con encapsulación"""


class Contact:
    """
    Clase que representa un contacto.

    Atributos:
        nombre (str): Nombre del contacto
        telefono (str): Teléfono del contacto
        email (str): Email del contacto
        direccion (str): Dirección del contacto
    """

    def __init__(self, nombre: str, telefono: str, email: str, direccion: str):
        self._nombre = nombre
        self._telefono = telefono
        self._email = email
        self._direccion = direccion

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def telefono(self) -> str:
        return self._telefono

    @property
    def email(self) -> str:
        return self._email

    @property
    def direccion(self) -> str:
        return self._direccion

    @nombre.setter
    def nombre(self, valor: str):
        if not valor.strip():
            raise ValueError("El nombre no puede estar vacío")
        self._nombre = valor

    @email.setter
    def email(self, valor: str):
        if not valor.strip():
            raise ValueError("El email no puede estar vacío")
        self._email = valor

    @direccion.setter
    def direccion(self, valor: str):
        if not valor.strip():
            raise ValueError("La dirección no puede estar vacía")
        self._direccion = valor

    def __str__(self) -> str:
        return (
            f"Nombre: {self._nombre}\n"
            f"Teléfono: {self._telefono}\n"
            f"Email: {self._email}\n"
            f"Dirección: {self._direccion}"
        )

    def __repr__(self) -> str:
        return f"Contact('{self._nombre}', '{self._telefono}', '{self._email}', '{self._direccion}')"

    def to_dict(self) -> dict:
        return {
            "nombre": self._nombre,
            "telefono": self._telefono,
            "email": self._email,
            "direccion": self._direccion,
        }

    @staticmethod
    def from_dict(data: dict) -> "Contact":
        return Contact(
            data["nombre"],
            data["telefono"],
            data["email"],
            data["direccion"],
        )

# PRUEBA TÉCNICA BACKEND

> [!NOTE]
> **Diseñado y desarrollado por:**  
> Iván Alberto Sánchez Carrillo
> **Descarga la documentación de usuario en:**  
> (https://docs.google.com/document/d/1QYgjWC7bDdbA0xCOKu9ZJMmOsJmhee2tjmyLjjFYwC8/edit?usp=sharing)

## Descripción  
Este proyecto es una prueba técnica de conocimientos para Corporativo Madd Systems.  
Consiste en una aplicación web con un CRUD completo para usuarios y personajes, obteniendo los datos directamente de una API pública de personajes de la serie *Rick & Morty*.

## Tecnologías utilizadas
- **Lenguaje:** Python 3.12+
- **Framework:** Django & Django REST Framework (DRF)
- **Base de datos:** SQLite (por defecto para desarrollo)
- **Arquitectura:** Monolito Modular basado en MVT / Service Layer

## ¿Por qué estas tecnologías?  
El uso de **Python** y **Django** fue seleccionado conforme a los requerimientos especificados en la prueba técnica. Se implementó una **arquitectura modular** aprovechando el sistema de apps de Django (`users`, `roles`, `character`), parta mantener una separación clara de responsabilidades.

## Requisitos previos
- **Python** instalado en el equipo (versión 3.10 o superior).
- **MySQL** instalado en el equipo.

## Recomendaciónes de extenciones para visualizar mejor el codigo
- **Better Comments**
- **Error Lens**
- **Material Icon Theme**

## Instalación
Sigue estos pasos para configurar y ejecutar el proyecto en tu entorno local:

1. Clona el repositorio:
   ```bash
   git clone https://github.com/IvanSDec/prueba_tecnica_backend.git

2. Crear y activar el entorno virtual:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate

3. Instalar dependencias:
    ```bash
    pip install -r requirements.txt
    asegurate de tener ya tu .env creado y conf en este paso

4. **IMPORTANTE** Ejecuta el comando para crear la base de datos en MySQL:
    ```bash
    python manage.py createdatabase
    en caso de que no funcione crear manualmente la base de datos

5. Aplicar las migraciones a la base de datos:
    ```bash
    python manage.py migrate

6. Ejecutar el servidor de desarrollo:
    ```bash
    python manage.py runserver

> [!IMPORTANT]
>   Si tienes alguna duda, no dudes en contactarme:
> 
>   [![Instagram](https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://www.instagram.com/ivanscarrillomx/)
> 
>   [![Facebook](https://img.shields.io/badge/Facebook-1877F2?style=for-the-badge&logo=facebook&logoColor=white)](https://www.facebook.com/profile.php?id=100001168921982)
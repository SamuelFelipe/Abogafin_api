# Abogafin API

Abogafin es un aplicativo web que ayuda a las personas de a pie a encontrar
fácilmente la asesoría de un abogado certificado.
Con el fin de garantizar la satisfación de los usuarios los abogados aquí
registrados han de contar una licencia profecional activa además de que contaran
con una calificación dada por los usuarios que previamente hayan trabajado con el.

## Infraestructura

El aproximamiento de esta aplicación es monolitica, aunque por la estructura de Django
esta se puede separar en microservicios fácilmente.

## Stack

Para esta aplicación se va a utilizar Django Rest Framework, junto con Selenium el cual
se encargará de el proceso de verificación de las tarjetas profesionales de los abogados
inscritos en la plataforma.

Con el fin de tener una personalización mayor en las entidades principales se han creado
usuarios distintos al `BaseUser` que provee Django por defecto.

# Documentación de Arquitectura y Decisiones Técnicas – Sistema de Reservas de Recursos

## 1. Visión General

El sistema implementa un **backend para la gestión de reservas de recursos empresariales** (salas de reuniones, vehículos, equipamientos) usando **Django** y **Django REST Framework (DRF)**. Proporciona una API REST completa para consultar recursos, disponibilidad, realizar reservas y gestionar aprobaciones y cancelaciones.

### 1.1 Objetivos Principales

- Consultar y listar recursos.
- Consultar disponibilidad detallada.
- Gestionar reservas con validación de conflictos.
- Manejar aprobación de reservas y diferentes roles de usuario.
- Gestionar políticas de cancelación.

## 2. Arquitectura General

El sistema sigue un enfoque **modular y en capas**, facilitando su escalabilidad, mantenimiento y extensibilidad. La arquitectura se organiza en:

### 2.1 Modelos de Dominio (`apps/resources/models.py`)

- Representan recursos y políticas de cancelación.
- Recursos con atributos específicos según su tipo (capacidad, horarios, aforo compartido).

### 2.2 Servicios / Casos de Uso (`apps/reservations/services`)

- Contienen la lógica de negocio central: disponibilidad, solapamientos, políticas de cancelación y aforo compartido.
- Aíslan la lógica compleja de los endpoints, facilitando pruebas unitarias.

### 2.3 Serializers y Views (`apps/resources/serializers.py`, `apps/resources/views.py`)

- Serializan modelos a JSON para la API.
- Validan datos y encapsulan reglas mínimas de negocio.

### 2.4 Endpoints REST (`urls.py`)

- `/api/resources/`: lista recursos.
- `/api/resources/{id}/`: consulta disponibilidad y creación de reservas.
- `/api/reservations/`: aprobación y cancelación de reservas.

### 2.5 Autenticación y Roles

- Usuarios tipo trabajador y responsable.
- Token-based authentication para pruebas.
- Reglas diferenciadas según rol (aprobación automática o pendiente).

## 3. Modelado de Recursos

Se adoptó un **patrón de herencia polimórfica** con un modelo base `Resource` y subtipos:

- **MeetingRoom:** capacidad, aforo compartido, reservas por horas.
- **Vehicle:** reservas por días completos.
- **Equipment:** reservas por horas o días.

Este enfoque busca la escalabilidad para añadir nuevos tipos de recurso, manteniendo la lógica específica por tipo sin duplicación de código.

## 4. Gestión de Disponibilidad y Reservas

- La disponibilidad se calcula considerando:
  - Reservas existentes y solapamientos.
  - Capacidad y aforo compartido.
  - Estado de aprobación (pendiente o aprobada).
- El servicio central `CheckAvailabilityService` realiza validaciones:
  - Conflictos horarios completos y parciales.
  - Aforo restante para recursos compartidos.
  - Políticas de cancelación según recurso.

## 5. Políticas de Cancelación

Tres tipos implementados:

- **Flexible:** cancelación hasta 1h antes; transferible.
- **Moderada:** cancelación hasta 24h antes; transferible después del límite.
- **Bloqueada:** no cancelable ni transferible.

Cada política se encapsula en una clase independiente, siguiendo el patrón **Strategy**, lo que permite añadir nuevas políticas sin modificar la lógica central de reservas.

## 6. Flujo de Aprobación

- **Worker:** reservas quedan en estado `pending`.
- **Manager / Responsable:** puede crear reservas `approved` directamente.
- Disponibilidad refleja reservas `approved` y `pending` por separado.

## 7. Decisiones Técnicas Clave

1. **Separación de lógica de negocio y presentación**

    - Lógica de reservas, disponibilidad, aforo y cancelaciones implementada en servicios independientes de views y serializers, facilitando testabilidad, mantenimiento y reutilización.

2. **Polimorfismo para tipos de recursos**

   - Modelo base `Resource` con subtipos `MeetingRoom`, `Vehicle` y `Equipment`, evitando condicionales múltiples y permitiendo extender el sistema fácilmente.

3. **Validaciones centralizadas en servicios**

   - Validaciones de solapamientos, aforo y políticas de cancelación concentradas en `services`, garantizando consistencia de datos y reduciendo duplicación.

4. **Políticas de cancelación como estrategia**

   - Cada política (`Flexible`, `Moderada`, `Bloqueada`) implementada como clase independiente, permitiendo añadir o modificar políticas sin tocar la lógica central.

5. **Roles diferenciados y flujo de aprobación**

   - Roles de trabajador y responsable, asegurando integridad de reservas y evitando errores de autorización.

6. **Seeders de datos para pruebas**

   - Reservas aleatorias para tests y demostraciones, permitiendo probar disponibilidad y aforo de manera rápida y reproducible.

## 8. Endpoints Principales

| Endpoint | Método | Funcionalidad |
|----------|--------|---------------|
| `/api/resources/` | GET | Listar recursos con atributos. |
| `/api/resources/{id}/availability/` | GET | Consultar disponibilidad para fecha/hora. |
| `/api/resources/{id}/reservations/` | POST | Crear reserva (aprobación según rol). |
| `/api/reservations/{id}/approve/` | POST | Aprobar reserva pendiente (solo manager). |
| `/api/reservations/{id}/cancel/` | POST | Cancelar reserva según política. |

## 9. Testabilidad y Estrategias de Pruebas

Las pruebas cubren funcionalidades críticas: reservas, disponibilidad y políticas de cancelación, con unit tests para lógica de negocio y tests de integración para interacción entre componentes.

Se añaden seeding de recursos y reservas en entorno de test, permitiendo probar disponibilidad y solapamientos de manera controlada.

Se ha creado una **colección de Postman** para importar y facilitar la realización de tests manuales y de integración.

## 10. Conclusiones

La arquitectura se orienta a ofrecer un sistema sólido, flexible y sencillo de mantener, apoyado en un diseño modular que facilita su evolución futura, tanto en nuevos tipos de recursos como en políticas adicionales, sin comprometer la coherencia de datos ni las reglas de negocio. La separación de responsabilidades garantiza un crecimiento ordenado y una base fácil de extender.

Para evitar complejidad en esta fase, se decidió utilizar el modelo de usuario por defecto de Django, priorizando el avance en la funcionalidad principal de reservas. Del mismo modo, aunque se valoró separar las políticas de cancelación en una aplicación independiente, se optó por mantenerlas dentro de la app de recursos para conservar un alcance manejable y enfocado.

La autenticación se resolvió mediante un esquema simple basado en tokens. Aun así, la arquitectura queda preparada para incorporar mecanismos más robustos, como OAuth o JWT, si fuese necesario.

En conjunto, el sistema se ha construido con un enfoque pragmático: decisiones pensadas para mantener claridad y evitar sobreingeniería, sin renunciar a una estructura preparada para crecer de forma ordenada. El uso del modelo de usuario de Django, la centralización de políticas de cancelación y la autenticación básica permitieron concentrarse en la lógica de negocio, mientras que el diseño modular abre la puerta a incorporar nuevos recursos, reglas o mecanismos de seguridad sin reestructurar la base existente.

El objetivo principal ha sido establecer una base estable, mantenible y lista para evolucionar conforme aumenten los requisitos del sistema.

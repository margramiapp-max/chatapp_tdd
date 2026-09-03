# Aplicacion de chat con creacion de usuarios, Envio de mensajes y moderacion 

Este projecto implementa una creacion de perfiles de usuario, creado rigurosamente bajo la 
metodologia TDD

## Tecnologia utilizadas 
**Python 3.12**
**Flask** (Para construcción de la API REST)
**SQLite3** (inicialemte con almacenamiento de memoria compartida)
**Pytest & Pytest-Cov** (motor de pruebas y resporte estadistico de cobertura)
**GitHub Actions** (Integración Continua para ejecución automática de tests)

##Notas 
Para ejecutar las pruebas localmente y verificar la cobertura del 100%:
```bash
pytest --cov=. --cov-report=term-missing
```


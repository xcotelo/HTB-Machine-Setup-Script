# HTB Machine Setup Script

Pequeño script en Python para automatizar la preparación de una máquina de laboratorio (p. ej. HackTheBox).
Crea estructura de carpetas, añade la entrada en `/etc/hosts` y lanza una VPN. Al presionar `Ctrl+C` el script intenta limpiar la configuración (elimina la entrada añadida en `/etc/hosts`).

---

## Contenido

* `setup_htb.py` — script principal (pega el contenido del script que tengas).

---

## Requisitos

* Python 3.x
* `sudo` para:

  * modificar `/etc/hosts`
  * ejecutar `openvpn`
* `openvpn` instalado y el archivo de configuración `archivoHTB.ovpn` disponible en el directorio desde el que ejecutes el script (o ajusta la ruta en el script).
* Permisos para crear carpetas en `/home/USER` (el script usa rutas hardcodeadas).

---

## Instalación / Preparación

1. Crea un archivo, por ejemplo `setup_htb.py`, y pega el script.
2. (Opcional) Hazlo ejecutable:

```bash
chmod +x setup_htb.py
```

---

## Uso

Ejecuta desde terminal:

```bash
python3 setup_htb.py
```

El script pedirá:

* IP de la máquina (ej. `10.10.10.5`)
* Nombre de la máquina (ej. `maquina.htb`)

Qué hace automáticamente:

* Crea `/home/USER/HTB_<nombre_sin_.htb>` con subcarpetas `nmap`, `exploit`, `varios`.
* Añade la línea `IP nombre` a `/etc/hosts`.
* Lanza `sudo openvpn archivoHTB.ovpn` y se queda esperando.
* Si presionas `Ctrl+C`, intenta:

  * Detener la VPN.
  * Eliminar la entrada añadida en `/etc/hosts`.

---

## Advertencias / Seguridad

* ⚠️ **Modifica `/etc/hosts`**: el script añade y elimina líneas en `/etc/hosts`. Revisa siempre el contenido del archivo antes de ejecutar.
* ⚠️ **Rutas hardcodeadas**: `/home/USER/...` y `archivoHTB.ovpn` están fijadas en el script. Cámbialas según tu usuario y estructura.
* ⚠️ **Ejecución con sudo**: el script invoca `sudo` para acciones privilegiadas; se te solicitará contraseña si corresponde.
* El limpiador elimina las líneas que contienen la IP indicada; si el mismo IP aparece para otras entradas, podrían verse afectadas. Revisa manualmente `/etc/hosts` si dudas.

---

## Ejemplo rápido

1. `python3 setup_htb.py`
2. Input:

```
Introduce la IP de la máquina de HTB: 10.10.10.5
Introduce un nombre para la máquina (ej: maquina.htb): merda.htb
```

3. Verás confirmaciones:

```
✓ Entrada añadida a /etc/hosts
✓ IP 10.10.10.5 guardada en target
✓ Configuración completada. Carpeta creada en /home/USSE/HTB_maquina
Iniciando conexión VPN...
```

4. Cuando quieras terminar: `Ctrl+C` → limpieza automática.

---

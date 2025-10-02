# HTB Machine Setup Script

Pequeño script en Python para automatizar la preparación de una máquina de laboratorio (p. ej. HackTheBox).
Crea estructura de carpetas, añade la entrada en `/etc/hosts`, guarda la IP en un archivo `target` (útil para polybar) y lanza una VPN. Al presionar `Ctrl+C` el script intenta limpiar la configuración (elimina la entrada añadida en `/etc/hosts` y vacía el archivo `target`).

---

## Contenido

* `setup_htb.py` — script principal (pega el contenido del script que tengas).

---

## Requisitos

* Python 3.x
* `sudo` para:

  * modificar `/etc/hosts`
  * ejecutar `openvpn`
* `openvpn` instalado y el archivo de configuración `lab_xcotelo.ovpn` disponible en el directorio desde el que ejecutes el script (o ajusta la ruta en el script).
* Permisos para crear carpetas en `/home/xian` (el script usa rutas hardcodeadas).

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
* Nombre de la máquina (ej. `merda.htb`)

Qué hace automáticamente:

* Crea `/home/xian/HTB_<nombre_sin_.htb>` con subcarpetas `nmap`, `exploit`, `varios`.
* Añade la línea `IP nombre` a `/etc/hosts`.
* Guarda la IP en `/home/xian/.config/bin/target`.
* Lanza `sudo openvpn lab_xcotelo.ovpn` y se queda esperando.
* Si presionas `Ctrl+C`, intenta:

  * Detener la VPN.
  * Eliminar la entrada añadida en `/etc/hosts`.
  * Vaciar `/home/xian/.config/bin/target`.

---

## Advertencias / Seguridad

* ⚠️ **Modifica `/etc/hosts`**: el script añade y elimina líneas en `/etc/hosts`. Revisa siempre el contenido del archivo antes de ejecutar.
* ⚠️ **Rutas hardcodeadas**: `/home/xian/...` y `lab_xcotelo.ovpn` están fijadas en el script. Cámbialas según tu usuario y estructura.
* ⚠️ **Ejecución con sudo**: el script invoca `sudo` para acciones privilegiadas; se te solicitará contraseña si corresponde.
* El limpiador elimina las líneas que contienen la IP indicada; si el mismo IP aparece para otras entradas, podrían verse afectadas. Revisa manualmente `/etc/hosts` si dudas.

---

## Personalización recomendada

* Cambiar `target_file_path` y la base de `ruta_base` para que se adapten a tu usuario (p. ej. usar `~` o `os.path.expanduser("~")`).
* Usar un archivo de configuración (JSON/YAML) para evitar rutas hardcodeadas.
* Añadir validaciones de IP y nombre.
* Implementar backup de `/etc/hosts` antes de modificarlo.

---

## Ejemplo rápido

1. `python3 setup_htb.py`
2. Input:

```
Introduce la IP de la máquina de HTB: 10.10.10.5
Introduce un nombre para la máquina (ej: merda.htb): merda.htb
```

3. Verás confirmaciones:

```
✓ Entrada añadida a /etc/hosts
✓ IP 10.10.10.5 guardada en target
✓ Configuración completada. Carpeta creada en /home/xian/HTB_merda
Iniciando conexión VPN...
```

4. Cuando quieras terminar: `Ctrl+C` → limpieza automática.

---

import os
import subprocess
import signal
import sys
import time

# Variable global para la IP
ip = ""

def cleanup_target(signum, frame):
    print("\n\n⏹️  Limpiando configuración...")
    
    target_file_path = "/home/xian/.config/bin/target"
    try:
        with open(target_file_path, "w") as target_file:
            target_file.write("")
        print("✓ Target limpiado")
    except Exception as e:
        print(f"✗ Error limpiando target: {e}")
    
    # Limpiar la entrada específica de /etc/hosts
    try:
        # Leer todo el contenido
        with open("/etc/hosts", "r") as f:
            content = f.read()
        
        # Remover la línea que contiene la IP (la última que añadimos)
        lines = content.split('\n')
        new_lines = [line for line in lines if ip not in line]
        
        # Escribir de vuelta sin la línea de nuestra IP
        with open("/etc/hosts", "w") as f:
            f.write('\n'.join(new_lines))
        
        print(f"✓ Entrada de {ip} removida de /etc/hosts")
    except Exception as e:
        print(f"✗ Error limpiando /etc/hosts: {e}")
    
    print("¡Hasta luego! 🚀")
    sys.exit(0)

# Registrar el manejador de señales
signal.signal(signal.SIGINT, cleanup_target)

# Pedir datos al usuario
try:
    ip = input("Introduce la IP de la máquina de HTB: ").strip()
    nombre = input("Introduce un nombre para la máquina (ej: merda.htb): ").strip()
except KeyboardInterrupt:
    cleanup_target(signal.SIGINT, None)

# Quitar la extensión .htb para la carpeta
nombre_carpeta = nombre.replace(".htb", "")

# Ruta base donde se creará la carpeta "HTB_nombre"
ruta_base = os.path.expanduser(f"/home/xian/HTB_{nombre_carpeta}")

# Subcarpetas a crear dentro de "HTB"
subcarpetas = ["nmap", "exploit", "varios"]

# Crear carpeta principal
os.makedirs(ruta_base, exist_ok=True)

# Crear subcarpetas dentro de "HTB"
for carpeta in subcarpetas:
    ruta_sub = os.path.join(ruta_base, carpeta)
    os.makedirs(ruta_sub, exist_ok=True)

# Crear entrada en /etc/hosts (requiere permisos de sudo)
try:
    entrada = f"{ip} {nombre}\n"
    subprocess.run(["sudo", "bash", "-c", f"echo '{entrada}' >> /etc/hosts"], check=True)
    print("✓ Entrada añadida a /etc/hosts")
except subprocess.CalledProcessError as e:
    print(f"✗ Error añadiendo a /etc/hosts: {e}")

# Guardar la IP en el archivo target para polybar
target_file_path = "/home/xian/.config/bin/target"
try:
    # Asegurarse de que el directorio existe
    os.makedirs(os.path.dirname(target_file_path), exist_ok=True)
    # Escribir la IP en el archivo target
    with open(target_file_path, "w") as target_file:
        target_file.write(ip)
    print(f"✓ IP {ip} guardada en target")
except Exception as e:
    print(f"✗ Error guardando target: {e}")

print(f"✓ Configuración completada. Carpeta creada en {ruta_base}")
print("\n💡 Presiona Ctrl+C para detener la VPN y limpiar automáticamente")

# Iniciar conexión VPN
print("Iniciando conexión VPN...")
try:
    # Usar Popen y esperar manualmente para capturar Ctrl+C
    process = subprocess.Popen(["sudo", "openvpn", "lab_xcotelo.ovpn"])
    
    # Esperar de forma que podamos capturar Ctrl+C
    while process.poll() is None:
        time.sleep(0.5)  # Pequeña pausa para verificar estado
        
except KeyboardInterrupt:
    print("\n🛑 Capturando Ctrl+C...")
    
finally:
    # Siempre limpiar al salir, sin importar cómo terminemos
    if 'process' in locals() and process.poll() is None:
        print("Deteniendo proceso VPN...")
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            print("Forzando cierre de VPN...")
            process.kill()
    
    cleanup_target(signal.SIGINT, None)
# 🛡️ Laboratorio: Implementación de RAID 5 en Ubuntu (VirtualBox)

## 👨‍💻 Autor
**Nombre:** Julián David Briñez Sánchez  
**Materia:** Sistemas Operativos / Administración de Servidores  
**Fecha:** _(colocar la fecha de entrega)_  

---

## 🧠 Objetivo
Implementar un arreglo **RAID 5 (paridad distribuida)** en una máquina virtual con Ubuntu utilizando **tres discos virtuales** adicionales. Entender cómo RAID 5 ofrece **tolerancia a fallos** (soporta la caída de 1 disco) con **mejor aprovechamiento de espacio** que RAID 1 y buen rendimiento en lectura.

---

## ⚙️ Requerimientos

- VirtualBox instalado.
- Ubuntu Server/Desktop.
- **1 disco principal** (SO) + **3 discos para el RAID 5** (p. ej., 1 GB cada uno): `/dev/sdb`, `/dev/sdc`, `/dev/sdd`.
- Paquete `mdadm` instalado.

> Si necesitas limpiar discos usados antes: `sudo wipefs -a /dev/sdX` o borra particiones con `fdisk` (opción `d` y luego `w`).

---

## 🧾 Paso a Paso

### 1) Agregar los discos en VirtualBox
**Configuración → Almacenamiento → Controlador SATA → Agregar disco** (crear 3 discos nuevos).
- Verifica en Ubuntu que aparezcan como `/dev/sdb`, `/dev/sdc`, `/dev/sdd`.

📸 **Pantallazo 1:** configuración de VirtualBox mostrando el SO + 3 discos.

---

### 2) Instalar herramientas
```bash
sudo apt update
sudo apt install mdadm -y
```

📸 **Pantallazo 2:** instalación correcta de `mdadm`.

---

### 3) Verificar discos disponibles
```bash
sudo fdisk -l
```
Deberías ver `/dev/sdb`, `/dev/sdc`, `/dev/sdd` sin formato.

📸 **Pantallazo 3:** salida de `fdisk -l` con los 3 discos.

---

### 4) Crear el RAID 5
```bash
sudo mdadm --create --verbose /dev/md0 --level=5 --raid-devices=3 /dev/sdb /dev/sdc /dev/sdd
```
- `--level=5` → RAID 5 (paridad distribuida).
- `--raid-devices=3` → tres discos mínimos.

📸 **Pantallazo 4:** confirmación de creación (cuando pide escribir `yes`).

---

### 5) Verificar sincronización y estado
```bash
cat /proc/mdstat
sudo mdadm --detail /dev/md0
```
Espera a que termine el **reshaping/sync** inicial o continúa (se puede usar mientras sincroniza).

📸 **Pantallazo 5:** `/proc/mdstat` mostrando progreso y `--detail` con los 3 discos activos.

---

### 6) Crear sistema de archivos y montar
```bash
sudo mkfs.ext4 /dev/md0
sudo mkdir -p /mnt/raid5
sudo mount /dev/md0 /mnt/raid5
df -h | grep md0
```
📸 **Pantallazo 6:** `df -h` mostrando `/dev/md0` montado en `/mnt/raid5`.

---

### 7) Probar funcionamiento
```bash
sudo cp /etc/hostname /mnt/raid5/
ls -l /mnt/raid5
```
📸 **Pantallazo 7:** archivo visible dentro de `/mnt/raid5`.

---

### 8) Montaje automático (opcional recomendado)
Obtener UUID:
```bash
sudo blkid /dev/md0
```
Editar `/etc/fstab` y añadir (reemplaza el UUID):
```
UUID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx  /mnt/raid5  ext4  defaults  0  0
```
Prueba:
```bash
sudo umount /mnt/raid5
sudo mount -a
df -h | grep md0
```
📸 **Pantallazo 8:** entrada agregada en `fstab` y montaje correcto.

---

### 9) Guardar la config de mdadm
```bash
sudo mdadm --detail --scan | sudo tee -a /etc/mdadm/mdadm.conf
sudo update-initramfs -u
```
📸 **Pantallazo 9:** comandos ejecutados sin errores.

---

## 🧪 (Opcional) Simular fallo y recuperación

### A) Marcar disco como fallado y retirarlo
```bash
sudo mdadm --manage /dev/md0 --fail /dev/sdc
sudo mdadm --manage /dev/md0 --remove /dev/sdc
cat /proc/mdstat
sudo mdadm --detail /dev/md0
```
📸 **Pantallazo 10:** estado degradado (un disco `failed/removed`).

### B) Añadir disco de reemplazo
(Agrega un nuevo disco en VirtualBox → aparecerá como `/dev/sde`)
```bash
sudo mdadm --manage /dev/md0 --add /dev/sde
cat /proc/mdstat
sudo mdadm --detail /dev/md0
```
📸 **Pantallazo 11:** reconstrucción en progreso y luego estado óptimo.

> Mientras **solo un** disco esté caído, RAID 5 mantiene los datos disponibles gracias a la **paridad**.

---

## ⚙️ (Opcional) Salud y chequeo de paridad
Forzar verificación de paridad:
```bash
echo check | sudo tee /sys/block/md0/md/sync_action
cat /proc/mdstat
```
Cancelar (si fuera necesario):
```bash
echo idle | sudo tee /sys/block/md0/md/sync_action
```

---

## 📈 (Opcional) Pruebas rápidas de rendimiento
```bash
# Escritura secuencial (100 MiB)
sudo dd if=/dev/zero of=/mnt/raid5/testfile bs=1M count=100 oflag=direct

# Lectura
sudo dd if=/mnt/raid5/testfile of=/dev/null bs=1M iflag=direct
```
📸 **Pantallazo 12:** velocidades reportadas por `dd` (lectura suele ser muy buena en RAID 5).

---

## 🧮 Cálculo de capacidad útil
Capacidad ≈ (**N - 1**) × tamaño de disco.  
Con 3 discos de 1 GB → ≈ **2 GB** útiles.

---

## 🧾 Conclusiones
- **RAID 5** ofrece **tolerancia a fallos** (1 disco) con **buen equilibrio** entre rendimiento y espacio.
- La **lectura** es rápida; la **escritura** puede ser más costosa por el cálculo de paridad.
- Recomendado para almacenamiento donde se requiere disponibilidad y eficiencia, no para bases de datos muy transaccionales.

---

## 📚 Referencias
- `man mdadm`
- https://man7.org/linux/man-pages/man8/mdadm.8.html
- https://help.ubuntu.com/community/Installation/SoftwareRAID

---

> 💡 **Consejo:**  
> Convierte este README a PDF para entrega:
> ```bash
> pandoc README_RAID5.md -o RAID5_Laboratorio.pdf
> ```

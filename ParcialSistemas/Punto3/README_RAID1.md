# 🧩 Laboratorio: Implementación de RAID 1 en Ubuntu (VirtualBox)

## 👨‍💻 Autor
**Nombre:** Julián David Briñez Sánchez  
**Materia:** Sistemas Operativos / Administración de Servidores  
**Fecha:** _(colocar la fecha de entrega)_  

---

## 🧠 Objetivo
Implementar un arreglo **RAID 1 (espejo)** en una máquina virtual con Ubuntu utilizando discos virtuales adicionales, con el fin de comprender cómo funciona la replicación de datos y la tolerancia a fallos en sistemas Linux.

---

## ⚙️ Requerimientos

- VirtualBox instalado.
- Imagen ISO de **Ubuntu Server o Desktop**.
- **1 disco principal** (para el sistema operativo).
- **2 discos adicionales** (para el RAID 1), por ejemplo de 1 GB cada uno.
- Paquete `mdadm` instalado.

---

## 🧾 Paso a Paso

### 1. Agregar los discos virtuales

Abrir **Configuración → Almacenamiento → Controlador SATA → Agregar disco duro → Crear nuevo disco**  
- Crear dos discos nuevos de 1 GB cada uno.  
- Verificar que aparezcan como `/dev/sdb` y `/dev/sdc` dentro de Ubuntu.

📸 **Pantallazo 1:** configuración de VirtualBox mostrando los 3 discos (sistema + 2 adicionales).

---

### 2. Instalar `mdadm`

En la terminal ejecutar:

```bash
sudo apt update
sudo apt install mdadm -y
```

📸 **Pantallazo 2:** instalación exitosa del paquete `mdadm`.

---

### 3. Verificar los discos disponibles

```bash
sudo fdisk -l
```

Deberían aparecer `/dev/sdb` y `/dev/sdc` como discos sin formato.

📸 **Pantallazo 3:** salida del comando `fdisk -l` mostrando los discos.

---

### 4. Crear el RAID 1

```bash
sudo mdadm --create --verbose /dev/md0 --level=1 --raid-devices=2 /dev/sdb /dev/sdc
```

- `/dev/md0` es el nuevo dispositivo RAID.
- `--level=1` indica que es un espejo (RAID 1).
- `--raid-devices=2` indica dos discos.

📸 **Pantallazo 4:** confirmación de creación del RAID (cuando pide escribir “yes”).

---

### 5. Verificar el estado del RAID

```bash
cat /proc/mdstat
```

y/o

```bash
sudo mdadm --detail /dev/md0
```

📸 **Pantallazo 5:** resultado del estado del RAID mostrando los discos activos y la sincronización.

---

### 6. Formatear y montar el RAID

Formatear con `ext4`:
```bash
sudo mkfs.ext4 /dev/md0
```

Montar en `/mnt/raid1`:
```bash
sudo mkdir /mnt/raid1
sudo mount /dev/md0 /mnt/raid1
```

📸 **Pantallazo 6:** salida de `df -h` mostrando `/dev/md0` montado.

---

### 7. Probar el RAID

Copia un archivo dentro del RAID:
```bash
sudo cp /etc/hostname /mnt/raid1/
```

Verifica:
```bash
ls /mnt/raid1
```

📸 **Pantallazo 7:** contenido de `/mnt/raid1` mostrando el archivo copiado.

---

### 8. Hacer el montaje permanente (opcional)

Obtener UUID:
```bash
sudo blkid /dev/md0
```

Editar el archivo `/etc/fstab`:
```bash
sudo nano /etc/fstab
```

Agregar la línea:
```
UUID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx  /mnt/raid1  ext4  defaults  0  0
```

📸 **Pantallazo 8:** línea añadida al final del archivo `/etc/fstab`.

---

### 9. Guardar la configuración del RAID

```bash
sudo mdadm --detail --scan | sudo tee -a /etc/mdadm/mdadm.conf
sudo update-initramfs -u
```

📸 **Pantallazo 9:** comando ejecutado correctamente sin errores.

---

### 10. (Opcional) Simular un fallo de disco

```bash
sudo mdadm --manage /dev/md0 --fail /dev/sdb
sudo mdadm --manage /dev/md0 --remove /dev/sdb
```

📸 **Pantallazo 10:** salida mostrando `/dev/sdb` como "failed".

Reemplazar el disco y añadir uno nuevo:
```bash
sudo mdadm --manage /dev/md0 --add /dev/sdd
```

📸 **Pantallazo 11:** estado del RAID restaurado con el nuevo disco.

---

## 🧾 Conclusiones

- El RAID 1 permite mantener **copias idénticas de los datos** en ambos discos, garantizando la **tolerancia a fallos**.  
- En caso de que uno de los discos falle, los datos permanecen accesibles en el otro.  
- `mdadm` es una herramienta potente y versátil para gestionar arreglos RAID por software en Linux.  
- Este laboratorio demuestra la importancia de la **redundancia** en los sistemas de almacenamiento.

---

## 📚 Referencias

- [Documentación oficial de mdadm](https://man7.org/linux/man-pages/man8/mdadm.8.html)
- [Ubuntu RAID Guide](https://help.ubuntu.com/community/Installation/SoftwareRAID)

---

> 💡 **Consejo:**  
> Puedes convertir este README.md en PDF para entrega con:
> ```bash
> pandoc README.md -o RAID1_Laboratorio.pdf
> ```

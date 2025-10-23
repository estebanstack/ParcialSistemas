# ⚡ Laboratorio: Implementación de RAID 0 en Ubuntu (VirtualBox)

## 👨‍💻 Autor
**Nombre:** Julián David Briñez Sánchez  
**Materia:** Sistemas Operativos / Administración de Servidores  
**Fecha:** _(colocar la fecha de entrega)_  

---

## 🧠 Objetivo
Implementar un arreglo **RAID 0 (striping)** en una máquina virtual con Ubuntu utilizando discos virtuales adicionales, con el fin de comprender el funcionamiento de la división de datos y el aumento del rendimiento en sistemas Linux.

---

## ⚙️ Requerimientos

- VirtualBox instalado.
- Imagen ISO de **Ubuntu Server o Desktop**.
- **1 disco principal** (para el sistema operativo).
- **2 discos adicionales** (para el RAID 0), por ejemplo de 1 GB cada uno.
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

### 4. Crear el RAID 0

```bash
sudo mdadm --create --verbose /dev/md0 --level=0 --raid-devices=2 /dev/sdb /dev/sdc
```

- `/dev/md0` es el nuevo dispositivo RAID.
- `--level=0` indica que es un **RAID 0 (striping)**.
- `--raid-devices=2` indica dos discos.

📸 **Pantallazo 4:** confirmación de creación del RAID 0 (cuando pide escribir “yes”).

---

### 5. Verificar el estado del RAID

```bash
cat /proc/mdstat
```

y/o

```bash
sudo mdadm --detail /dev/md0
```

📸 **Pantallazo 5:** resultado del estado del RAID mostrando los discos activos.

---

### 6. Formatear y montar el RAID

Formatear con `ext4`:
```bash
sudo mkfs.ext4 /dev/md0
```

Montar en `/mnt/raid0`:
```bash
sudo mkdir /mnt/raid0
sudo mount /dev/md0 /mnt/raid0
```

📸 **Pantallazo 6:** salida de `df -h` mostrando `/dev/md0` montado.

---

### 7. Probar el RAID

Copia un archivo dentro del RAID:
```bash
sudo cp /etc/hostname /mnt/raid0/
```

Verifica:
```bash
ls /mnt/raid0
```

📸 **Pantallazo 7:** contenido de `/mnt/raid0` mostrando el archivo copiado.

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
UUID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx  /mnt/raid0  ext4  defaults  0  0
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

### 10. (Opcional) Probar rendimiento

```bash
sudo dd if=/dev/zero of=/mnt/raid0/testfile bs=1M count=100
```

📸 **Pantallazo 10:** resultado mostrando la velocidad de escritura (debería ser superior a un disco individual).

---

## 🧾 Conclusiones

- El **RAID 0** mejora significativamente el **rendimiento de lectura y escritura** al dividir los datos entre varios discos.  
- No ofrece **tolerancia a fallos**: si un disco falla, se pierde toda la información.  
- Es ideal para entornos donde la **velocidad** es prioritaria sobre la seguridad (por ejemplo, procesamiento de video o simulaciones).  
- `mdadm` facilita la creación, administración y supervisión de arreglos RAID por software en Linux.

---

## 📚 Referencias

- [Documentación oficial de mdadm](https://man7.org/linux/man-pages/man8/mdadm.8.html)
- [Ubuntu RAID Guide](https://help.ubuntu.com/community/Installation/SoftwareRAID)

---

> 💡 **Consejo:**  
> Puedes convertir este README.md en PDF para entrega con:
> ```bash
> pandoc README_RAID0.md -o RAID0_Laboratorio.pdf
> ```

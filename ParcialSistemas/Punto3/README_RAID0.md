# Implementación de RAID 0 en Ubuntu

---

## Objetivo
Implementar un arreglo **RAID 0 (striping)** en una máquina virtual con Ubuntu utilizando discos virtuales adicionales, con el fin de comprender el funcionamiento de la división de datos y el aumento del rendimiento en sistemas Linux.

---


## Paso a Paso

### 1. Agregar los discos virtuales

Abrir **Configuración → Almacenamiento → Controlador SATA → Agregar disco duro → Crear nuevo disco**  
- Crear dos discos nuevos de 1 GB cada uno.  
- Verificar que aparezcan como `/dev/sdb` y `/dev/sdc` dentro de Ubuntu.

<img width="519" height="171" alt="image" src="https://github.com/user-attachments/assets/fa7d4013-f79d-4d8b-ad54-d158cc813443" />

---

### 2. Instalar `mdadm`

En la terminal ejecutar:

```bash
sudo apt update
sudo apt install mdadm -y
```
---

### 3. Verificar los discos disponibles

```bash
sudo fdisk -l
```

Deberían aparecer `/dev/sdb` y `/dev/sdc` como discos sin formato.

<img width="633" height="315" alt="image" src="https://github.com/user-attachments/assets/36160f2a-c046-4439-a4d0-7b6aa92f1f1d" />

---

### 4. Crear el RAID 0

```bash
sudo mdadm --create --verbose /dev/md0 --level=0 --raid-devices=2 /dev/sdb /dev/sdc
```

- `/dev/md0` es el nuevo dispositivo RAID.
- `--level=0` indica que es un **RAID 0 (striping)**.
- `--raid-devices=2` indica dos discos.

<img width="834" height="111" alt="image" src="https://github.com/user-attachments/assets/fc6bbdf1-f46d-440b-b914-bca60ebfba7a" />

---

### 5. Verificar el estado del RAID

```bash
cat /proc/mdstat
```

y/o

```bash
sudo mdadm --detail /dev/md0
```

<img width="789" height="131" alt="image" src="https://github.com/user-attachments/assets/9052fa90-b9cb-458f-9ee5-83071c9253fa" />

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

<img width="816" height="552" alt="image" src="https://github.com/user-attachments/assets/69bc28cc-398c-4325-b80e-32194d5bc647" />

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

<img width="548" height="68" alt="image" src="https://github.com/user-attachments/assets/109473ed-e121-4cdc-9ea3-2fb8e5025bb4" />

---

## Conclusiones

- El **RAID 0** mejora significativamente el **rendimiento de lectura y escritura** al dividir los datos entre varios discos.  
- No ofrece **tolerancia a fallos**: si un disco falla, se pierde toda la información.  
- Es ideal para entornos donde la **velocidad** es prioritaria sobre la seguridad (por ejemplo, procesamiento de video o simulaciones).  


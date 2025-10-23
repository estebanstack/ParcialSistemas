# Implementación de RAID 1 en Ubuntu


---

## Objetivo
Implementar un arreglo **RAID 1** en una máquina virtual con Ubuntu utilizando discos virtuales adicionales, con el fin de comprender cómo funciona la replicación de datos y la tolerancia a fallos en sistemas Linux.

---

## Paso a Paso

### 1. Agregar los discos virtuales

Abrir **Configuración → Almacenamiento → Controlador SATA → Agregar disco duro → Crear nuevo disco**  
- Crear dos discos nuevos de 1 GB cada uno.  
- Verificar que aparezcan como `/dev/sdb` y `/dev/sdc` dentro de Ubuntu.

<img width="465" height="148" alt="image" src="https://github.com/user-attachments/assets/8daa86b9-f845-4133-b392-37793f13ea01" />

---

### 2. Instalar `mdadm`

En la terminal ejecutar:

```bash
sudo apt update
sudo apt install mdadm -y
```

<img width="1018" height="463" alt="image" src="https://github.com/user-attachments/assets/af6074b2-8194-4ccc-a84b-e6d0da748ea0" />

---

### 3. Verificar los discos disponibles

```bash
sudo fdisk -l
```

Deberían aparecer `/dev/sdb` y `/dev/sdc` como discos sin formato.

<img width="659" height="286" alt="image" src="https://github.com/user-attachments/assets/b63d47e7-a4b5-46fb-8d2c-82c2cc869620" />


---

### 4. Crear el RAID 1

```bash
sudo mdadm --create --verbose /dev/md0 --level=1 --raid-devices=2 /dev/sdb /dev/sdc
```

- `/dev/md0` es el nuevo dispositivo RAID.
- `--level=1` indica que es un espejo (RAID 1).
- `--raid-devices=2` indica dos discos.

<img width="1031" height="241" alt="image" src="https://github.com/user-attachments/assets/7ae557c1-432a-48f7-9769-4de4dab1664e" />

---

### 5. Verificar el estado del RAID

```bash
cat /proc/mdstat
```

y/o

```bash
sudo mdadm --detail /dev/md0
```

<img width="996" height="264" alt="image" src="https://github.com/user-attachments/assets/17d32f5c-b250-4f3c-9881-3af97dabbdde" />

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

<img width="867" height="511" alt="image" src="https://github.com/user-attachments/assets/8f51a822-73cb-4f75-b2fb-c1f8dd23d98c" />

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

<img width="554" height="72" alt="image" src="https://github.com/user-attachments/assets/0fa385a7-dd7c-4cce-92d2-e1a417b25da0" />


---

### 8. Guardar la configuración del RAID

```bash
sudo mdadm --detail --scan | sudo tee -a /etc/mdadm/mdadm.conf
sudo update-initramfs -u
```

<img width="860" height="57" alt="image" src="https://github.com/user-attachments/assets/205133f3-afbe-4df1-aab9-a54f75a23d67" />

---
### 9. Prueba desmontar raid 1

<img width="550" height="66" alt="image" src="https://github.com/user-attachments/assets/d4a7edec-b9b1-4125-85ba-b22ac180e815" />
<img width="891" height="552" alt="image" src="https://github.com/user-attachments/assets/fa6db2c9-3939-49b5-a2e6-8ef2a32904b9" />


## Conclusiones

- El RAID 1 permite mantener **copias idénticas de los datos** en ambos discos, garantizando la **tolerancia a fallos**
- En caso de que uno de los discos falle, los datos permanecen accesibles en el otro  
- `mdadm` es una herramienta potente y versátil para gestionar arreglos RAID por software en Linux  



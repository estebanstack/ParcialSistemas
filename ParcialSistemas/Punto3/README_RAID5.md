# Implementación de RAID 5 en Ubuntu

---

## Objetivo
Implementar un arreglo **RAID 5 (paridad distribuida)** en una máquina virtual con Ubuntu utilizando **tres discos virtuales** adicionales. Entender cómo RAID 5 ofrece **tolerancia a fallos** (soporta la caída de 1 disco) con **mejor aprovechamiento de espacio** que RAID 1 y buen rendimiento en lectura.

---

## Paso a Paso

### 1) Agregar los discos en VirtualBox
**Configuración → Almacenamiento → Controlador SATA → Agregar disco** (crear 3 discos nuevos).
- Verifica en Ubuntu que aparezcan como `/dev/sdb`, `/dev/sdc`, `/dev/sdd`.

<img width="536" height="181" alt="image" src="https://github.com/user-attachments/assets/3edd95d4-fb55-495a-a979-131e713c53a3" />

---

### 2) Instalar herramientas
```bash
sudo apt update
sudo apt install mdadm -y
```

---

### 3) Verificar discos disponibles
```bash
sudo fdisk -l
```
<img width="679" height="444" alt="image" src="https://github.com/user-attachments/assets/e28b8795-51fd-404a-8791-a698c5048942" />

---

### 4) Crear el RAID 5
```bash
sudo mdadm --create --verbose /dev/md0 --level=5 --raid-devices=3 /dev/sdb /dev/sdc /dev/sdd
```
- `--level=5` → RAID 5 (paridad distribuida).
- `--raid-devices=3` → tres discos mínimos.

<img width="737" height="180" alt="image" src="https://github.com/user-attachments/assets/2b447959-1c43-4a44-b0ea-e773356e49ab" />

---

### 5) Verificar sincronización y estado
```bash
cat /proc/mdstat
sudo mdadm --detail /dev/md0
```

<img width="737" height="176" alt="image" src="https://github.com/user-attachments/assets/96f9b422-e23e-4f2b-93da-5c396bc8b481" />

---

### 6) Crear sistema de archivos y montar
```bash
sudo mkfs.ext4 /dev/md0
sudo mkdir -p /mnt/raid5
sudo mount /dev/md0 /mnt/raid5
df -h | grep md0
```
<img width="743" height="501" alt="image" src="https://github.com/user-attachments/assets/3e293560-dad9-4733-a2a7-8d2462d85672" />

---

### 7) Probar funcionamiento
```bash
sudo cp /etc/hostname /mnt/raid5/
ls -l /mnt/raid5
```
<img width="607" height="137" alt="image" src="https://github.com/user-attachments/assets/cb969e98-9420-4307-bf3f-1c4b8f1c2f7f" />

---

## Cálculo de capacidad útil
Capacidad ≈ (**N - 1**) × tamaño de disco.  
Con 3 discos de 1 GB → ≈ **2 GB** útiles.

---

## Conclusiones
- **RAID 5** ofrece **tolerancia a fallos** (1 disco) con **buen equilibrio** entre rendimiento y espacio.
- La **lectura** es rápida; la **escritura** puede ser más costosa por el cálculo de paridad.
- Recomendado para almacenamiento donde se requiere disponibilidad y eficiencia, no para bases de datos muy transaccionales.


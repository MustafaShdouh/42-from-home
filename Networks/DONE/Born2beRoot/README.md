*This activity has been created as part of the 42 curriculum by mel-shdo.*

## Description
Born2beRoot is a System Administration related exercise designed to introduce the fundamentals of virtualization and server setup. The goal of this project is to create a first virtual machine in VirtualBox (or UTM) following strict instructions. It involves setting up a minimal server running Debian or Rocky Linux without a graphical user interface (GUI), configuring encrypted partitions using LVM, and implementing strong security policies including firewall configuration, secure SSH access, and robust password rules.

## Project Description
### Operating System Choice
For this project, the chosen operating system is **Debian**. 
- **Debian Advantages:** It is highly stable, user-friendly for beginners in system administration, has a massive repository of packages, and a large community for support. It uses the `apt` package manager which is widely documented.
- **Rocky Linux Advantages:** It is a downstream, complete binary-compatible release using the Red Hat Enterprise Linux (RHEL) operating system source code, making it an excellent choice for enterprise-level server environments.
- **Why Debian?** Debian was chosen because it is highly recommended for users new to system administration due to its simplicity, extensive documentation, and straightforward setup process (like AppArmor) compared to the more complex configuration required for Rocky (like KDump and SELinux).

### Main Design Choices
- **Partitioning:** Created at least 2 encrypted partitions using Logical Volume Manager (LVM) to ensure data security and flexible disk management.
- **Security Policies:**
  - **Firewall:** Configured `UFW` to leave only port 4242 open.
  - **SSH:** Set up an SSH service on port 4242 while disabling remote root login for security reasons.
  - **Password Policy:** Implemented a strong password policy requiring 30-day expiration, 2-day minimum change interval, 7-day warning, and a minimum length of 10 characters comprising uppercase, lowercase, and numeric characters, without consecutive identical characters or the username.
- **User Management:** Created a non-root user belonging to the `user42` and `sudo` groups, configured `sudo` with strict rules (limited paths, max 3 authentication attempts, custom error message, and logging to `/var/log/sudo/`, TTY mode enabled).
- **Services Installed:** Minimal services including SSH server, UFW, AppArmor, and a custom bash script (`monitoring.sh`) scheduled via cron to broadcast system information every 10 minutes.

### Comparisons
#### Debian vs Rocky Linux
- **Debian** is a community-driven Linux distribution known for its stability and the `apt` package manager. It is very adaptable and great for general-purpose servers.
- **Rocky Linux** is a downstream build of RHEL (Red Hat Enterprise Linux). It is designed to be a solid, predictable, and enterprise-grade OS, typically using `dnf`/`yum`. 

#### AppArmor vs SELinux
- **AppArmor** (used in Debian) is a Mandatory Access Control (MAC) system that uses path-based rules to restrict programs' capabilities. It is generally considered easier to configure and maintain.
- **SELinux** (used in Rocky) is a more fine-grained, label-based MAC system developed by the NSA. It provides deeper security but comes with a steeper learning curve.

#### UFW vs firewalld
- **UFW (Uncomplicated Firewall)** is the default firewall configuration tool for Ubuntu/Debian. It aims to provide an easy-to-use interface for iptables.
- **firewalld** is the default firewall management tool for Rocky/RHEL. It supports network/firewall zones and provides a dynamically managed firewall with support for D-Bus.

#### VirtualBox vs UTM
- **VirtualBox** is an open-source, cross-platform virtualization software from Oracle. It is widely used and supports a vast array of guest operating systems.
- **UTM** is a virtualization app specifically for macOS (especially Apple Silicon M1/M2 Macs) that uses the native Apple Hypervisor and QEMU to run virtual machines.

## Instructions
### Installation and Setup
1. **Prerequisites:** Install VirtualBox (or UTM if using an Apple Silicon Mac).
2. **Importing the VM:** Import the virtual machine image.
3. **Starting the VM:** Boot the virtual machine. The VM operates without a GUI.
4. **Login:** Log in with the provided user credentials or via SSH.

### Connecting via SSH
To connect to the server via SSH:
```bash
ssh -p 4242 <username>@<host_ip>
```
*Note: Root login over SSH is disabled.*

### Execution
The server runs a custom monitoring script automatically every 10 minutes using `cron`, which broadcasts system information (architecture, CPU, RAM, disk usage, active connections, etc.) to all terminals.

## Resources
- [Debian Documentation](https://www.debian.org/doc/)
- [VirtualBox Documentation](https://www.virtualbox.org/wiki/Documentation)
- [LVM - Logical Volume Manager](https://wiki.archlinux.org/title/LVM)
- [UFW Essentials](https://www.digitalocean.com/community/tutorials/ufw-essentials-common-firewall-rules-and-commands)
- [AppArmor Documentation](https://gitlab.com/apparmor/apparmor/-/wikis/Documentation)
- **AI Usage:** AI was used to generate this README file to properly structure the documentation, descriptions, and comparisons based on the Born2beRoot project requirements.

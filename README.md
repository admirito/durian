# Durian Debian Deployer

Durian is a set of tools to automate the installation of a Debian based operating system, specifically Ubuntu. You can create a partial Debian package archive mirror, easily setup PXE network booting and define several customized templates. Finally, you can deploy a system with just one single command. The deployment could be done on a physical or a virtual machine.

The main advantage of durian over pervasive could provisioning software is its independencey from disk images. A machine could be defined with a simple human-readable description in less than a few kilobytes. The definition could be deployed in a few minutes. It might be a bit slower than deploying a premade disk image but the deployment will always use the up-to-date software packages so you don't need to upgrade the software after the deployment.

Durian is inspired from [Fully Automatic Installation] [1] (FAI), although, it uses Debian installation [preseeds] [2] rather than using ts own installation process. It is merely a tool to easily setup the environment, automates the generation of debian preseed files and the deployment process.

Durian currently supports libvirt virtual machine deployment, so you can easly create and deploy a KVM virtual machine with a single command. Durian is higly extedible with simple plugins. So you can easily fulfill your own requirements.

### Version
1.0.0

### Installation

On Ubuntu:

```sh
$ sudo add-apt-repository ppa:mrazavi/durian
$ sudo apt-get update
$ sudo apt-get install durian
```

### Plugins

Main plugins are:

* mkboot - make necessary files for network booting (pxe)
* mkmirror - make a local mirror for apt packages
* deploy - make a host ready for deployment

To find out about other plugins just execute durian without any argumetns.

```sh
$ durian
```

Or read druian plugins source code as examples to get an idea how to write your own plugins.

### Usage Example

```sh
$ sudo apt-get install tftpd-hpa dnsmasq
```
Update dnsmasq configurations to set PXE booting from durian machine.
Then setup the environment:
```sh
$ sudo durian mkboot /var/lib/tftpboot
$ sudo durian mkmirror /var/www
```
Define your templates in *~/.durian/definitions*. Look at */usr/share/durian/definitions* for examples. You can include any of the seeds listed by the command:
```sh
$ durian list seeds
```
Finally, deploy a definiton by its name (e.g. for ubuntu-server.cfg in */usr/share/durian/definitions* on a machine with *00:11:22:33:44:55:66* hardware MAC address):
```sh
$ durian deploy ubuntu-server 00:11:22:33:44:55:66
```
And boot the system with PXE network booting, or you can deploy right into a new created VM with:
```sh
$ durian deploy -e ubuntu-server vm
```
*-e* makes deploy command interactive. So you can customize your VM hardware specification.

### Development

Want to contribute? Great!

Contact me at mrazavi64 at g-mail.

### Todo's

The source code currently only includes configurations to deploy ubuntu 14.04 amd64 server. The first job is to add configurations for other Ubuntu and Debian releases.

License
----

GPLv3


[1]:http://fai-project.org/
[2]:https://wiki.debian.org/DebianInstaller/Preseed
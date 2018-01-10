Title: Why does linux du command print no result and occupy one 100 CPU usage
Date: 2017-05-24 21:15
Tags: du,mtab,bind,Linux,Centos
Category: Blog
Slug: Why-does-linux-du-command-print-no-result-and-occupy-one-100-CPU-usage
Author: zhoudshu

## The Problem

  Today, My colleague found an abnormal problem and asked me the reason. I recorded the following analysis steps. 

  This problem is that linux du command does not print the results, and at the same time, the process of du command occupies 100% CPU usage. Result of top command is the following:

```bash
# top
  PID USER      PR  NI  VIRT  RES  SHR S %CPU %MEM    TIME+  COMMAND                                                                                                    
36343 root      20   0  110m  13m 1780 R 99.8  0.0   1:37.66 du                                                                                                         
36370 root      20   0  110m  13m 1780 R 94.2  0.0   1:20.98 du
   86 root      RT   0     0    0    0 S  1.3  0.0 134:21.57 migration/11                                                                                               
  107 root      RT   0     0    0    0 S  1.3  0.0 354:38.81 migration/14                                                                                               
  268 root      RT   0     0    0    0 S  1.3  0.0 328:32.61 migration/37                                                                                               
   36 root      RT   0     0    0    0 S  1.0  0.0 347:16.40 migration/4                                                                                                
  142 root      RT   0     0    0    0 S  1.0  0.0 385:43.15 migration/19                                                                                               
  156 root      RT   0     0    0    0 S  1.0  0.0 304:55.27 migration/21                                                                                               
  170 root      RT   0     0    0    0 S  1.0  0.0 292:30.41 migration/23                                                                                               
  981 root       0 -20     0    0    0 S  1.0  0.0 371:15.84 kworker/0:1H
```

## what happened does du command
   I used the strace command to find what happened the du limit. I found a lot of stat lines about "/var/named/chroot/usr/lib64/bind". According to the records about "open("/etc/mtab", O_RDONLY)             = 3", I known du command reads the system file of "/etc/mtab". I confirmed the conclusion by seeing that file. There are above 70,000 lines about the same lines in mtab file, and this mtab file has 4.2M bytes size. 


```bash
# strace -o du.txt -p 36370
#

execve("/usr/bin/du", ["du", "command"], [/* 23 vars */]) = 0
brk(0)                                  = 0x96f000
mmap(NULL, 4096, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7f140cf02000
access("/etc/ld.so.preload", R_OK)      = -1 ENOENT (No such file or directory)
open("/etc/ld.so.cache", O_RDONLY)      = 3
fstat(3, {st_mode=S_IFREG|0644, st_size=25756, ...}) = 0
mmap(NULL, 25756, PROT_READ, MAP_PRIVATE, 3, 0) = 0x7f140cefb000
close(3)                                = 0
open("/lib64/libc.so.6", O_RDONLY)      = 3
read(3, "\177ELF\2\1\1\3\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0p\356\341\0060\0\0\0"..., 832) = 832
fstat(3, {st_mode=S_IFREG|0755, st_size=1926520, ...}) = 0
mmap(0x3006e00000, 3750152, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0x3006e00000
mprotect(0x3006f8a000, 2097152, PROT_NONE) = 0
mmap(0x300718a000, 20480, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x18a000) = 0x300718a000
mmap(0x300718f000, 18696, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_ANONYMOUS, -1, 0) = 0x300718f000
close(3)                                = 0
mmap(NULL, 4096, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7f140cefa000
mmap(NULL, 4096, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7f140cef9000
mmap(NULL, 4096, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7f140cef8000
arch_prctl(ARCH_SET_FS, 0x7f140cef9700) = 0
mprotect(0x300718a000, 16384, PROT_READ) = 0
mprotect(0x3006c1f000, 4096, PROT_READ) = 0
munmap(0x7f140cefb000, 25756)           = 0
brk(0)                                  = 0x96f000
brk(0x990000)                           = 0x990000
open("/usr/lib/locale/locale-archive", O_RDONLY) = 3
fstat(3, {st_mode=S_IFREG|0644, st_size=99154480, ...}) = 0
mmap(NULL, 99154480, PROT_READ, MAP_PRIVATE, 3, 0) = 0x7f1407068000
close(3)                                = 0
open("/etc/mtab", O_RDONLY)             = 3
fstat(3, {st_mode=S_IFREG|0644, st_size=3711287, ...}) = 0
mmap(NULL, 4096, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7f140cf01000
read(3, "/doev/sda2 / ext4 rw 0 0\nproc /pr"..., 4096) = 4096
read(3, " /var/named/chroot/etc/named non"..., 4096) = 4096
read(3, "ed/chroot/usr/lib64/bind none rw"..., 4096) = 4096
read(3, "/etc/named none rw,bind 0 0\n/usr"..., 4096) = 4096
read(3, "4/bind none rw,bind 0 0\n/etc/nam"..., 4096) = 4096
read(3, ",bind 0 0\n/usr/lib64/bind /var/n"..., 4096) = 4096
read(3, "d 0 0\n/etc/named /var/named/chro"..., 4096) = 4096
read(3, "64/bind /var/named/chroot/usr/li"..., 4096) = 4096
tat("/var/named/chroot/etc/named", {st_mode=S_IFDIR|0750, st_size=4096, ...}) = 0
stat("/var/named/chroot/usr/lib64/bind", {st_mode=S_IFDIR|0755, st_size=4096, ...}) = 0
stat("/var/named/chroot/etc/named", {st_mode=S_IFDIR|0750, st_size=4096, ...}) = 0
stat("/var/named/chroot/usr/lib64/bind", {st_mode=S_IFDIR|0755, st_size=4096, ...}) = 0
stat("/var/named/chroot/etc/named", {st_mode=S_IFDIR|0750, st_size=4096, ...}) = 0
stat("/var/named/chroot/usr/lib64/bind", {st_mode=S_IFDIR|0755, st_size=4096, ...}) = 0
stat("/var/named/chroot/etc/named", {st_mode=S_IFDIR|0750, st_size=4096, ...}) = 0
stat("/var/named/chroot/usr/lib64/bind", {st_mode=S_IFDIR|0755, st_size=4096, ...}) = 0
stat("/var/named/chroot/etc/named", {st_mode=S_IFDIR|0750, st_size=4096, ...}) = 0

```

```bash
# cat /etc/mtab

/dev/sda2 / ext4 rw 0 0
proc /proc proc rw 0 0
sysfs /sys sysfs rw 0 0
devpts /dev/pts devpts rw,gid=5,mode=620 0 0
/dev/sdb1 /data/proclog ext4 rw 0 0
/dev/sda1 /boot ext4 rw 0 0
tmpfs /dev/shm tmpfs rw 0 0
/dev/sda5 /data/cache1 ext4 rw 0 0
/dev/sdb2 /data/cache2 ext4 rw 0 0
/dev/sdc /data/cache3 ext4 rw 0 0
/dev/sdd /data/cache4 ext4 rw 0 0
/dev/sde /data/cache5 ext4 rw 0 0
/dev/sdf /data/cache6 ext4 rw 0 0
/dev/sdg /data/cache7 ext4 rw 0 0
/dev/sdh /data/cache8 ext4 rw 0 0
/dev/sdi /data/cache9 ext4 rw 0 0
/dev/sdj /data/cache10 ext4 rw 0 0
/dev/sdk /data/cache11 ext4 rw 0 0
/dev/sdl /data/cache12 ext4 rw 0 0
/etc/named /var/named/chroot/etc/named none rw,bind 0 0
/usr/lib64/bind /var/named/chroot/usr/lib64/bind none rw,bind 0 0
/etc/named /var/named/chroot/etc/named none rw,bind 0 0
/usr/lib64/bind /var/named/chroot/usr/lib64/bind none rw,bind 0 0
/etc/named /var/named/chroot/etc/named none rw,bind 0 0
/usr/lib64/bind /var/named/chroot/usr/lib64/bind none rw,bind 0 0
/etc/named /var/named/chroot/etc/named none rw,bind 0 0
/usr/lib64/bind /var/named/chroot/usr/lib64/bind none rw,bind 0 0
/etc/named /var/named/chroot/etc/named none rw,bind 0 0
/usr/lib64/bind /var/named/chroot/usr/lib64/bind none rw,bind 0 0
/etc/named /var/named/chroot/etc/named none rw,bind 0 0
/usr/lib64/bind /var/named/chroot/usr/lib64/bind none rw,bind 0 0
....
....
....

```

```bash
# ll -h /etc/mtab
-rw-r--r-- 1 root root 4.2M May 24 21:00 /etc/mtab

```
## The conclusion 
 du command reads system mtab file and uses the linux stat command to display file or file system status. if mtab line has many lines. du spend a lot of time and cpu to statistis file size. so We must let mtab file is one small file.
 
## mtab introduction
 mtab lists currently mounted file systems and is used by the mount and unmount commands when you want to list your mounts or unmount all. It is not used by the kernel, which maintains its own list (in /proc/mounts or /proc/self/mounts). Its structure is the same as fstab

## The running environment

* Nginx
* Bind 9.8.2+
* Java 1.7.0+
* Linux 2.6.32-573.el6.x86_6
* Centos 6.6+

## Good luck

#!/bin/sh


if [ -z "$1" ]; then
    echo "Please indicate a command":
    exit 1;
fi

if [ -z "$2" ]; then
    echo "Please indicate a user":
    exit 1;
fi




if [ "$1" = "create" ]; then
	fallocate -l 10M /home/container_$2.img && 
	dd if=/dev/zero bs=1M count=10 of=/home/container_$2.img && 

	if cryptsetup luksFormat /home/container_$2.img ; then
		exit 0
	else
    	exit 1
	fi
fi

if [ "$1" = "remove" ]; then
	rm -fr /home/container_$2.img
fi

if [ "$1" = "open" ]; then
	cryptsetup luksOpen /home/container_$2.img device_$2 || exit 3;
	file -sL /dev/mapper/device_$2|grep "data$" && mkfs.ext4 /dev/mapper/device_$2;
	mkdir -p /home/$2 &&
	mount /dev/mapper/device_$2 /home/$2 && 
	chown $2 /home/$2
fi

if [ "$1" = "close" ]; then
	umount /home/$2 && 
	cryptsetup luksClose device_$2
fi

if [ "$1" = "exists" ]; then
	test -e /home/container_$2.img || exit 1
fi

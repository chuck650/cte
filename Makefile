bridge    = ovs-vlan
bridge_ip = 10.223.45.1/24
bridge_net = 10.223.45.0/24
inventory = inventory.yaml

ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

.PHONY: clean network stop show all

help:
	@printf "make [TARGET]\n"

clean: stop
	@printf "Removing all networking and device infrastructure\n"
	@sudo virsh net-undefine $(bridge)
	@sudo ovs-vsctl del-br $(bridge)

network:
	@printf "Provisioning networking infrastructure on localhost\n"
	@ansible-playbook -v -i $(ROOT_DIR)/$(inventory) $(ROOT_DIR)/playbooks/provision_host.yml

multipass:
	@printf "Provisioning multipass on localhost"
	@ansible-playbook -v -i $(ROOT_DIR)/$(inventory) $(ROOT_DIR)/playbooks/multipass.yml

all: network show
	@printf "Provisioning all infrastructure\n"

stop:
	@sudo virsh net-destroy $(bridge)

show:
	@printf "\nOpenvSwitch Configuration\n"
	@sudo ovs-vsctl show
	# | awk '/^\s*Bridge $(bridge)/ {br=1} /^\s*(?Bridge|ovs)/ {exit} {if(br){print $0}}' -
	@printf "\nLibvirt Network Information\n"
	@sudo virsh net-info
	# "$(bridge)"
	@printf "\nMultipass VM Information\n"
	@sudo multipass list

	@printf "\nLibvirt VM Information\n"
	@sudo virsh list --all

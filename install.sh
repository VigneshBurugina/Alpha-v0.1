#!/bin/bash
#Part of: Alpha-build-ver0.1
#Author: Vignesh Burugina


echo "Please run this as Superuser"
echo "Installing Alpha"
echo "Build-ver0.1"
mkdir ~/Documents/Invoices
sudo mv ./build-files/create-invoice /bin
sudo chmod +x /bin/create-invoice
sudo mv ./build-files/Invoice.pdf ~/Templates
sudo mv ./build-files/invoice.py /bin
echo 'Finished Copying Files'
echo 'Installing Dependencies'
sudo pip3 install -r /build-files/requirements.txt
echo 'Done!'
create-invoice help

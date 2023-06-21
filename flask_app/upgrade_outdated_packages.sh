#!/bin/bash
# Run this in your virtual environment to upgrade all outdated packages
outdated_packages_file="outdated_packages.txt"
upgraded_packages_file="upgraded_packages.txt"
timestamp=$(date +"%Y-%m-%d %H:%M:%S")

pip list --outdated >"$outdated_packages_file"
if awk '{print $1}' <"$outdated_packages_file" | xargs -n1 pip install --upgrade; then
    echo "All packages upgraded successfully"
    mv "$outdated_packages_file" "${upgraded_packages_file}_${timestamp}"
else
    echo "Failed to upgrade all packages"
fi

# Its best to reinstall all packages with a fresh virtual environment because if the depedency conflict errors

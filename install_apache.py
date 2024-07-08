# Python script to install Apache on apt based distros
# Author: jdk3410 
# Improvements: error handling with subprocess.CalledProcessError, use logging framework instead of print statements 
# Improvements: input validation for user commands, unit tests
# Improvements: run commands in github actions runner
# Improvements: non-linux distro specific

# Importing the subprocess module to run the shell commands
import subprocess 

try:
    # Install apache2 using apt-get
    subprocess.run(["sudo", "apt-get", "-y", "install", "apache2"]) 

    # Add a placeholder index.html file to the apache2 root directory and start it
    with open("/var/www/html/index.html", "w") as file:
        file.write(f"Hello World! from {subprocess.check_output('hostname').decode().strip()}")
    subprocess.run(["sudo", "systemctl", "start", "apache2"])

    # Ensure that apache2 starts on boot
    subprocess.run(["sudo", "systemctl", "enable", "apache2"])

    # If the script runs without any errors, print the following message
    print("Apache2 has been installed successfully!")

except Exception as e:
    # If the script has an error, print the line that errored out
    print("An error occurred while installing Apache2")
    print("Error:", e)

# End of script

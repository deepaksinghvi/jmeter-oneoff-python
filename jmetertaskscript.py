import os
import subprocess
import requests

import tarfile 
print('*****Downloading Apache Jmeter******')
  
print("*****Downloading Apache Jmeter******")

url = 'https://dlcdn.apache.org//jmeter/binaries/apache-jmeter-5.6.3.tgz'
jmetergz = requests.get(url, allow_redirects=True)
open('apache-jmeter-5.6.3.tgz', 'wb').write(jmetergz.content)

print("*****Downloading JDKr******")

url = 'https://download.oracle.com/java/17/latest/jdk-17_linux-x64_bin.tar.gz'
jdkgz = requests.get(url, allow_redirects=True)
open('jdk-17_linux-x64_bin.tar.gz', 'wb').write(jdkgz.content)
    

print("*****Extracting Apache Jmeter******")
# open file 
jmeterfile = tarfile.open('apache-jmeter-5.6.3.tgz') 
  
# extracting file 
jmeterfile.extractall('./') 
  
jmeterfile.close() 

print("*****Extracting JDK******")
# open file 
javafile = tarfile.open('jdk-17_linux-x64_bin.tar.gz') 
  
# extracting file 
javafile.extractall('./') 
  
javafile.close() 

#os.system('chown -R 777 ./apache-jmeter-5.6.3')
#os.system('chown -R 777 ./jdk-17.0.11')

# Set the JAVA_HOME environment variable
os.environ["JAVA_HOME"] = "./jdk-17.0.11"
# Set the JMETER_HOME environment variable
os.environ["JMETER_HOME"] = "./apache-jmeter-5.6.3"

os.environ["PATH"] = f"{os.environ['PATH']}:{os.environ['JMETER_HOME']}/bin"


os.environ["PATH"] = f"{os.environ['PATH']}:{os.environ['JMETER_HOME']}/bin"

print("*****PATH******")
print(os.environ["PATH"])
print(os.environ["SCRIPT_FILE_PATH"])
print(os.environ["SCRIPT_NAME"])

# Download the test script
if "SCRIPT_FILE_PATH" in os.environ and "SCRIPT_NAME" in os.environ:
    response = requests.get(os.environ["SCRIPT_FILE_PATH"])
    with open(f"./test/{os.environ['SCRIPT_NAME']}", "wb") as f:
        f.write(response.content)
else:
    print("SCRIPT_FILE_PATH or SCRIPT_NAME environment variable not set.")


# Run the JMeter test
subprocess.run(
    [
        "jmeter",
        "-n",
        "-t",
        f"./test/{os.environ['SCRIPT_NAME']}",
        "-l",
        "./csvreport/reports.csv",
        "-e",
        "-o",
        "./htmlreport",
    ],
    check=True,
)

print("*****RESULT START******")
print("reports.csv generated in csvreport")
print(subprocess.run(["ls", "-lrt", "./csvreport"], capture_output=True, text=True).stdout)

with open("./csvreport/reports.csv", "r") as f:
    print(f.read())

print("html report generated in htmlreport")
print(subprocess.run(["ls", "-lrt", "./htmlreport"], capture_output=True, text=True).stdout)

print("Execution Completed")
print("*****RESULT END******")

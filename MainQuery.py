# Blockchain Section
from Blockchain import Blockchain
# Firebase Section
from FirebaseHandler import FirebaseHandler
# Additional Section
from Telemetry import *
import os
import time
from datetime import datetime

def getMainData():
    pass

def main():
    print("==> Checking Keys")
    # Check Keys
    pubkeypem = os.path.exists("keys/pubkey.pem")
    privkeypem = os.path.exists("keys/privkey.pem")
    if(pubkeypem == True and privkeypem == True):
        print("==> Keys Found")
        print("==> Connecting to Firebase\n")
        ref = FirebaseHandler.connectDB() # Connect Once
        hash = None
        # Session set
        t_date = "SD_"+datetime.now().strftime("%d-%m-%Y")
        t_time = "ST_"+datetime.now().strftime("%H:%M:%S")
        for id in range(1,11):
            data = {}   # Re-init Data
            telemetry = {} # Re-init Telemetry
            print(f"==> Querying Block {str(id).zfill(4)}",end="",flush=True)
            # Block Chain
            if(hash is None):
                previous = "None"
            else:
                # Get Link via Hash
                previous = hash
            # Block Transaction
            if(id == 1):
                # First Block
                data.update({"0-0 Data Block":"First Block"})
            else:
                # Main Data
                data.update({"0-0 Data Block":f"Block {str(id).zfill(4)}"})

            # Telemetry - User
            user,uid,gid = Telemetry.getUserInfo()
            telemetry.update({"1-0 User":
                            {"1-1 Username":Blockchain.encryptMessage(user),
                            "1-2 UID":Blockchain.encryptMessage(uid),
                            "1-3 GID":Blockchain.encryptMessage(gid)
                            }})

            # Telemetry - Machine
            system,release,machine,arch,kernel = Telemetry.getMachineInfo()
            telemetry.update({"2-0 Machine":
                            {"2-1 System":Blockchain.encryptMessage(system),
                            "2-2 Release":Blockchain.encryptMessage(release),
                            "2-3 Machine":Blockchain.encryptMessage(machine),
                            "2-4 Architecture":Blockchain.encryptMessage(arch),
                            "2-5 Kernel":Blockchain.encryptMessage(kernel)
                            }})

            # Telemetry - Benchmark
            cpu_percent,memory_percent,text_usage,data_usage,cpu_temp = Telemetry.getBenchmarkInfo()
            telemetry.update({"3-0 Benchmark":
                            {"3-1 CPU Percent":Blockchain.encryptMessage(cpu_percent),
                            "3-2 Memory Percent":Blockchain.encryptMessage(memory_percent),
                            "3-3 Text Usage":Blockchain.encryptMessage(text_usage),
                            "3-4 Data Usage":Blockchain.encryptMessage(data_usage),
                            "3-5 CPU Temp":Blockchain.encryptMessage(cpu_temp)
                            }})

            # Telemetry - Network
            interface,ipaddr = Telemetry.getNetworkInfo()
            telemetry.update({"4-0 Network":
                            {"4-1 Interface":Blockchain.encryptMessage(interface),
                            "4-2 IP Address":Blockchain.encryptMessage(ipaddr)
                            }})

            # Telemetry - Date Time
            day,date,timenow,tzname = Telemetry.getDateTimeInfo()
            telemetry.update({"5-0 Datetime":
                            {"5-1 Day":Blockchain.encryptMessage(day),
                            "5-2 Date":Blockchain.encryptMessage(date),
                            "5-3 Time":Blockchain.encryptMessage(timenow),
                            "5-4 Timezone":Blockchain.encryptMessage(tzname)
                            }})

            data.update({f"0-1 Telemetry {str(id).zfill(4)}":telemetry})
            # Block Encapsulation
            block = Blockchain(previous,data)
            hash = Blockchain.getHash(block)
            block.setHash(hash)
            # DB Query
            FirebaseHandler.insertData(ref,t_date,t_time,id,block)
            print(" > [DONE]")
            time.sleep(10)
        print("\n==> Finished\n")
    else:
        print("==> Missing Keys")
        print("==> Aborted\n")

if __name__ == '__main__':
    main()

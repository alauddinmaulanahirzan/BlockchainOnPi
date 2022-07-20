# Firebase Section
from FirebaseHandler import FirebaseHandler
# Blockchain Section
from Blockchain import Blockchain
# Additional Section
import os

def main():
    valid = 0
    invalid = 0
    curHash = None
    print("==> Checking Keys")
    # Check Keys
    pubkeypem = os.path.exists("keys/pubkey.pem")
    privkeypem = os.path.exists("keys/privkey.pem")
    if(pubkeypem == True and privkeypem == True):
        print("==> Keys Found")
        print("==> Connecting to Firebase\n")
        ref = FirebaseHandler.connectDB() # Connect Once
        db = ref.get()
        # Iterate per machine
        for machine in db.keys():   # By Machine
            sessions = ref.child(machine).get()
            for session in sessions.keys():    #By Session
                times = ref.child(machine).child(session).get()
                for t_time in times.keys():    #By Session
                    blocks = ref.child(machine).child(session).child(t_time).get()
                    for block in blocks.keys():     # By Blocks
                        block_data = ref.child(machine).child(session).child(t_time).child(block).get()
                        print("==> Location /"+machine+"/"+session+"/"+t_time+"/"+block+":")
                        if(block_data["01 Previous"] == "None"):
                            curHash = block_data["03 Hash"]
                            valid += 1
                        else:
                            if(curHash == block_data["01 Previous"]):
                                curHash = block_data["03 Hash"]
                                valid += 1
                            else:
                                curHash = block_data["03 Hash"]
                                invalid += 1
                        if(block_data["01 Previous"] == "None"):
                            print("====> Previous :\t"+block_data["01 Previous"]) # String
                        else:
                            print("====> Previous :\t"+block_data["01 Previous"][:10]) # String
                        for data_key,data_value in block_data["02 Data"].items():    # Dictionary
                            print("====> "+data_key+" :\t"+Blockchain.decryptMessage(str(data_value)))
                        print("====> Hash :\t"+block_data["03 Hash"][:10])    # String
                        print("")
        print("=== Result ===")
        print(f"Valid Block : {valid}")
        print(f"Invalid Block : {invalid}")
    else:
        print("==> Missing Keys")
        print("==> Aborted")


if __name__ == '__main__':
    main()

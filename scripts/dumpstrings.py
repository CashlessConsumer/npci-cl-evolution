import glob, os, re, subprocess
BASE="/home/workspace/Projects/npci-cl-evolution/data/extracted"
PAT=re.compile(r"npci|NPCI|CL_VERSION|CL_MESSAGES|CL_PROPERTIES|CL_SUB_VERSION|cl-messages|LITE_CL|GetLite|LiteBalance|CalculateChallenge|GetChallenge|secure_element|setAttestation|EnableUPILITE|OfflineNativeDefender|securestorage|HelloUPI|HELLO_|UPI_CIRCLE|ReservePay|CREDIT_LINE|CreditLine|Delegate|attemp|block", re.I)
samples={"com.phonepe.app@25.05.16.0":None,"com.phonepe.app@25.09.19.0":None,"com.phonepe.app@26.01.02.0":None,"com.phonepe.app@26.09.11.0":None,"gpay-latest":None}
for s in samples:
    d=f"{BASE}/{s}"; out=[]
    for dx in sorted(glob.glob(f"{d}/raw/app/classes*.dex")):
        txt=subprocess.run(f"strings -a '{dx}'",shell=True,capture_output=True,text=True).stdout
        out += [l for l in txt.splitlines() if PAT.search(l)]
    for so in glob.glob(f"{d}/raw/app/lib/*/libSecureComponent.so"):
        txt=subprocess.run(f"strings -a '{so}'",shell=True,capture_output=True,text=True).stdout
        out += [l for l in txt.splitlines() if PAT.search(l)]
    with open(f"{d}/npci_dex_strings.txt","w") as f:
        f.write("\n".join(out))
    print(s, len(out), "lines")

UPI Common Library Specification (CL v2.3-v1.8).md · GitHub

[Skip to content](https://gist.github.com/nk521/c476c7fef884fed3226e6bc809a80e8c#start-of-content)

Search Gists

 

Search Gists

[All gists](https://gist.github.com/discover)
[Back to GitHub](https://github.com)
[Sign in](https://gist.github.com/auth/github?return_to=https%3A%2F%2Fgist.github.com%2Fnk521%2Fc476c7fef884fed3226e6bc809a80e8c)
[Sign up](https://gist.github.com/join?return_to=https%3A%2F%2Fgist.github.com%2Fnk521%2Fc476c7fef884fed3226e6bc809a80e8c&source=header-gist)

[Sign in](https://gist.github.com/auth/github?return_to=https%3A%2F%2Fgist.github.com%2Fnk521%2Fc476c7fef884fed3226e6bc809a80e8c) [Sign up](https://gist.github.com/join?return_to=https%3A%2F%2Fgist.github.com%2Fnk521%2Fc476c7fef884fed3226e6bc809a80e8c&source=header-gist)

You signed in with another tab or window. Reload to refresh your session.
You signed out in another tab or window. Reload to refresh your session.
You switched accounts on another tab or window. Reload to refresh your session.
 

Dismiss alert

{{ message }}

Instantly share code, notes, and snippets.

[![@nk521](https://avatars.githubusercontent.com/u/30789322?s=64&v=4)](https://gist.github.com/nk521)

[nk521](https://gist.github.com/nk521)/**[UPI Common Library Specification (CL v2.3-v1.8).md](https://gist.github.com/nk521/c476c7fef884fed3226e6bc809a80e8c)**
===============================================================================================================================================================

Created
January 25, 2026 20:05

Show Gist options

* [Download ZIP](https://gist.github.com/nk521/c476c7fef884fed3226e6bc809a80e8c/archive/9c48e6c3aa50a95733ced2b7354232c0d242b416.zip)

* [Star

  0
  (0)](https://gist.github.com/login?return_to=https%3A%2F%2Fgist.github.com%2Fnk521%2Fc476c7fef884fed3226e6bc809a80e8c)You must be signed in to star a gist
* [Fork

  0
  (0)](https://gist.github.com/login?return_to=https%3A%2F%2Fgist.github.com%2Fnk521%2Fc476c7fef884fed3226e6bc809a80e8c)You must be signed in to fork a gist

* Embed

  Select an option
  ================

  + Embed
     Embed this gist in your website.
  + Share
     Copy sharable link for this gist.
  + Clone via HTTPS
     Clone using the web URL.

  No results found
  ----------------

  [Learn more about clone URLs](https://docs.github.com/articles/which-remote-url-should-i-use)

   
   

  Clone this repository at &lt;script src=&quot;https://gist.github.com/nk521/c476c7fef884fed3226e6bc809a80e8c.js&quot;&gt;&lt;/script&gt;
* Save nk521/c476c7fef884fed3226e6bc809a80e8c to your computer and use it in GitHub Desktop.

[Code](https://gist.github.com/nk521/c476c7fef884fed3226e6bc809a80e8c)
[Revisions
1](https://gist.github.com/nk521/c476c7fef884fed3226e6bc809a80e8c/revisions)

Embed

Select an option
================

* Embed
   Embed this gist in your website.
* Share
   Copy sharable link for this gist.
* Clone via HTTPS
   Clone using the web URL.

No results found
----------------

[Learn more about clone URLs](https://docs.github.com/articles/which-remote-url-should-i-use)

 
 

Clone this repository at &lt;script src=&quot;https://gist.github.com/nk521/c476c7fef884fed3226e6bc809a80e8c.js&quot;&gt;&lt;/script&gt;

Save nk521/c476c7fef884fed3226e6bc809a80e8c to your computer and use it in GitHub Desktop.

[Download ZIP](https://gist.github.com/nk521/c476c7fef884fed3226e6bc809a80e8c/archive/9c48e6c3aa50a95733ced2b7354232c0d242b416.zip)

[Raw](https://gist.github.com/nk521/c476c7fef884fed3226e6bc809a80e8c/raw/9c48e6c3aa50a95733ced2b7354232c0d242b416/UPI%2520Common%2520Library%2520Specification%2520(CL%2520v2.3-v1.8).md)

[**UPI Common Library Specification (CL v2.3-v1.8).md**](https://gist.github.com/nk521/c476c7fef884fed3226e6bc809a80e8c#file-upi-common-library-specification-cl-v2-3-v1-8-md)

UPI Common Library Specification (CL v2.3-v1.8)
===============================================

---

Abstract
--------

This document defines the internal workings of the Unified Payments Interface (UPI) Common Library (CL) as implemented by NPCI in versions **2.3-v1.8**. The CL, embedded in UPI apps, facilitates encryption of sensitive data, generates cryptographic challenges, and standardizes the PIN entry experience across applications via the `pinactivitycomponent`. This document aims to assist researchers and developers in understanding the CL's role, cryptographic flows, and transaction structure.

---

Table of Contents
-----------------

* [RFC: UPI Common Library Specification (CL v2.3-v1.8)](https://gist.github.com/nk521/c476c7fef884fed3226e6bc809a80e8c#RFC-UPI-Common-Library-Specification-CL-v23-v18)
  + [Abstract](https://gist.github.com/nk521/c476c7fef884fed3226e6bc809a80e8c#Abstract)
  + [Table of Contents](https://gist.github.com/nk521/c476c7fef884fed3226e6bc809a80e8c#Table-of-Contents)
  + [1. Introduction](https://gist.github.com/nk521/c476c7fef884fed3226e6bc809a80e8c#1-Introduction)
  + [2. PIN Activity Component](https://gist.github.com/nk521/c476c7fef884fed3226e6bc809a80e8c#2-PIN-Activity-Component)
  + [3. Challenge Generation (`K0`)](https://gist.github.com/nk521/c476c7fef884fed3226e6bc809a80e8c#3-Challenge-Generation-K0)
    - [3.1 Random Initialization and AES Encryption](https://gist.github.com/nk521/c476c7fef884fed3226e6bc809a80e8c#31-Random-Initialization-and-AES-Encryption)
    - [3.2 RSA Wrapping and Backend Challenge](https://gist.github.com/nk521/c476c7fef884fed3226e6bc809a80e8c#32-RSA-Wrapping-and-Backend-Challenge)
  + [4. Transaction Flow](https://gist.github.com/nk521/c476c7fef884fed3226e6bc809a80e8c#4-Transaction-Flow)
    - [4.1 Pipe String Format](https://gist.github.com/nk521/c476c7fef884fed3226e6bc809a80e8c#41-Pipe-String-Format)
    - [4.2 Hashing and GCM Encryption](https://gist.github.com/nk521/c476c7fef884fed3226e6bc809a80e8c#42-Hashing-and-GCM-Encryption)
    - [4.3 Final Payload Construction](https://gist.github.com/nk521/c476c7fef884fed3226e6bc809a80e8c#43-Final-Payload-Construction)
  + [5. Interaction with CL](https://gist.github.com/nk521/c476c7fef884fed3226e6bc809a80e8c#5-Interaction-with-CL)
    - [5.1 Extracting The CL Version](https://gist.github.com/nk521/c476c7fef884fed3226e6bc809a80e8c#51-Extracting-The-CL-Version)
    - [5.2 Interacting With `CLMain`](https://gist.github.com/nk521/c476c7fef884fed3226e6bc809a80e8c#52-Interacting-With-CLMain)
  + [6. Security Considerations](https://gist.github.com/nk521/c476c7fef884fed3226e6bc809a80e8c#6-Security-Considerations)
  + [7. References](https://gist.github.com/nk521/c476c7fef884fed3226e6bc809a80e8c#7-References)

---

1. Introduction
---------------

The UPI Common Library (CL) is a shared component used by UPI applications to securely transmit sensitive transaction data. The library abstracts encryption, session management and challenge management.

This document focuses on CL version **2.3-v1.8**. It outlines how challenges are generated, what constitutes a transaction, and how encryption is performed.

---

2. PIN Activity Component
-------------------------

NPCI’s `pinactivitycomponent`, packaged under `org.npci.upi.security.pinactivitycomponent`, is used by all UPI apps to present the PIN screen and interact with CL.

---

3. Challenge Generation (`k0`)
------------------------------

A challenge key (`k0`) is generated. This key is used for all transactions as a challenge and can be rotated.

### 3.1 Random Initialization and AES Encryption

The following elements are generated:

* `k0`: 32 bytes random lowercase hexstring
* `token`: 32 bytes random lowercase hexstring
* `date`: today's date as string in `dd/mm/yyyy` format
* `datak`: 32 bytes key used for CBC encryption
* `iv`: random 16 bytes for CBC mode

These values are AES-CBC encrypted with PKCS#7 padding and then base64 encoded. The AES key (`datak`) is then RSA-encrypted using a newly generated key pair. An encrypted set of variables are created that includes:

* Encrypted `k0`, `token`, `date`
* Encrypted `id` (initialised as `"0"`)
* Plain IV base64 encoded and named `random`
* Encrypted AES key named `datak`

Note

As per current testing `id` has always been set to 0.

See the following example pseudo code:

```
Generate a 2048-bit RSA key pair.
Generate a random 256-bit AES key.
Generate a random 16-byte IV.

Use the public key to initialize a RSA-OAEP session with SHA256 hash.
Encrypt the AES key.

Use the unencrypted AES key and IV to initialise AES in CBC mode.
Pad formatted date, k0, id (equals to 0), encrypted AES key and token using PKCS#7 padding to a multiple of 16 bytes.

Encrypt all of the padded data one by one.
```

```
import base64
from Cryptodome.Cipher import PKCS1_OAEP, AES
from Cryptodome.PublicKey import RSA
from Cryptodome.Hash import SHA256
from Cryptodome.Random import get_random_bytes

pvt = RSA.generate(2048).export_key().decode()
pub = pvt.public_key()

aes_key = get_random_bytes(32)
cipher_rsa = PKCS1_OAEP.new(pub, hashAlgo=SHA256)
encrypted_aes_key = cipher_rsa.encrypt(aes_key)
iv = get_random_bytes(16)

def enc(val: bytes):
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    pad_len = 16 - (len(val) % 16)
    padded = val + bytes([pad_len]) * pad_len
    return base64.b64encode(cipher.encrypt(padded)).decode()

date = enc(format.encode())
random = base64.b64encode(iv).decode()
k0 = enc(k0.encode())
id = enc(b"0")
datak = base64.b64encode(encrypted_aes_key).decode()
token = enc(token.encode())
```

These variables are then stored locally for session continuity.

### 3.2 RSA Wrapping and Backend Challenge

A pipe-delimited string is generated:

```
{token}|{k0}|{device_id}
```

This string is encrypted using RSA-OAEP with SHA-256 and MGF1. The public key is extracted from a CRT file bundled within the app APK.

```
cipher = PKCS1_OAEP.new(public_key, hashAlgo=SHA256, mgfunc=lambda x, y: SHA256.new(x).digest())
ciphertext = cipher.encrypt(pipe_string.encode())
```

The final challenge is constructed as:

```
{CL_VERSION}|{base64.b64encode(ciphertext)}
```

This is submitted via a POST request to the backend endpoint.

---

4. Transaction Flow
-------------------

Once the challenge is accepted, transactions may proceed. This document describes two transaction types:

* `pay`: Send to a VPA
* `reqBalEnq`: Request balance inquiry

### 4.1 Pipe String Format

The pipe string structure for transactions is:

```
{amount}|{transaction_id}|{payer}|{payee}|{app_id}|{phone_no}|{device_id_35}|{credType}
```

* For `reqBalEnq`: `amount`, `payer`, and `payee` are empty strings.
* The `device_id` is trimmed to its first 35 uppercase characters.
  > [!NOTE]
  > `device_id` is PSP specific. Some apps may generate fully random string as device id, some may use android device id, etc.
* The `phone_no` is E.164 formatted but without the `+` prefix.
* The `transaction_id` is provided by the UPI app's backend upon initialising a transaction.
* `payer` & `payee` are the VPAs in small case.
* `credType` is what sets the context of current transaction. It can be `pay`, `reqBalEnq`, etc.

### 4.2 Hashing and GCM Encryption

A SHA-256 hash is computed over the pipe string, prefixed by a random 12-byte IV. This hash is encrypted using AES-GCM with the session's `k0` as the key:

```
ciphertext = AESGCM(k0).encrypt(iv, sha256_digest, None)
```

The result is:

```
{pin}|{transaction_id}|{Base64(ciphertext)}|{Base64(iv)}
```

### 4.3 Final Payload Construction

The above intermediary string is encrypted using RSA-OAEP with the public key derived from a startup XML config:

```
encryptedBase64String = Base64(
  RSA-OAEP(
    "PIN|TXN_ID|AESGCM(
      SHA256(
        pipe_string
      )
    )|IV"
  )
)
final_payload = f"{CL_VERSION}|{encryptedBase64String}"
```

This final string is submitted to the backend for transaction processing.

---

5. Interaction with CL
----------------------

All previous sections discussed how `pinactivitycomponent` interacts with CL and how CL works internally. This section outlines how that behavior can be programmatically simulated using a supervised Java Virtual Machine in Python via [JPype1](https://github.com/jpype-project/jpype).

CL source code is never shared with third parties. Instead, they receive a compiled JAR, obfuscated using ProGuard. Because it is distributed as a standalone JAR, we can load and invoke it directly using JPype1 in Python.

Although the CL JAR is compiled using Java 8, it can still be loaded in newer JVMs, provided the JVM is started with the `-Xverify:none` flag. First, extract the JARs from the APK’s DEX files using `d2j-dex2jar` from the [dex2jar](https://github.com/pxb1988/dex2jar) project:

```
sh d2j-dex2jar.sh -o ./output_path/ classes.dex
```

Then initialize the JVM as follows:

```
if not jpype.isJVMStarted():
   jpype.startJVM(
      *["-Xverify:none"],
      jvmpath="/usr/lib/jvm/java-11-openjdk-amd64/lib/server/libjvm.so",
      classpath=[
         # Directory for static files (e.g., signer.crt)
         "./javaruntime",

         # All extracted JARs go here
         "./jars/classes-dex2jar.jar",
         "./jars/classes2-dex2jar.jar",
         "./jars/classesN-dex2jar.jar",

         "./jars/commons-logging-1.2.jar",
         "./phonepe/jars/apk/phonepe/json-20250517.jar",
      ],
      convertStrings=True,
   )
```

Note:

1. commons-logging is required for internal logging support.
   > Download: <https://archive.apache.org/dist/commons/logging/binaries/commons-logging-1.2-bin.zip>
2. json-20250517.jar is similarly needed for internal JSON parsing.
   > Download: <https://search.maven.org/remotecontent?filepath=org/json/json/20250517/json-20250517.jar>

### 5.1 Extracting The CL Version

`org.npci.upi.security.pinactivitycomponent` package defines a class called `CLConstants` which is not stripped and will have proper naming. We can just print a final static constant variable from here by -

```
def get_cl_versions(self) -> tuple[str, str]:
    clazz = jpype.JClass("org.npci.upi.security.pinactivitycomponent.CLConstants")
    return clazz.CL_VERSION, clazz.LITE_CL_VERSION
```

### 5.2 Interacting With `CLMain`

The primary class responsible for CL operations is located at:

```
in.org.npci.commonlibrary.b
```

For sanity, let's call it CLMain. It is initialized with an XML file that contains NPCI’s public keys:

```
_clMain = jpype.JClass("in.org.npci.commonlibrary.b")
clMain = _clMain(xmlSource)
```

The core method exposed by CLMain is:

```
public Message a(
    String code,
    String transaction_id,
    String pin,
    String pipe_string,
    String k0,
    Boolean is_upi_lite
)
```

Translated to Python usage:

```
message = clMain.a(code, transaction_id, pin, pipe_string, k0, is_upi_lite)
```

Where:

1. code is typically "NPCI" or "NPCI-LITE" (can be extracted from the xmlSource)
2. pipe\_string is formatted as:

   ```
   pipe_string = f"{amount}|{transaction_id}|{payer}|{payee}|{app_id}|{phone_no}|{device_id_35}|{credType}"
   ```

Once called, the method returns a `Message` object, from which you can extract the final encrypted payload:

```
encryptedBase64String: str = message.getData().getEncryptedBase64String()
final_payload = f"{CL_VERSION}|{encryptedBase64String}"
```

Note

`k0` challenge cannot be automated in a similar fashion because that would require emulating the entire Android runtime (ART) environment inside Python. Or at least, one will have write stubs for used Android packages/classes.

---

6. Security Considerations
--------------------------

* The CRT file embedded in APKs, despite being expired, is still considered valid as it is not listed in the official Certificate Revocation List (CRL).

---

7. References
-------------

1. CL v2.0 Specification Repository: <https://github.com/librefin-in/cl-specification>
2. CRL for NPCI Certificates: <https://idrbtca.org.in/crl_27B0.crl>
3. PyCryptodome documentation: <https://pycryptodome.readthedocs.io>
4. JPype1 documentation: <https://github.com/jpype-project/jpype>

[Sign up for free](https://gist.github.com/join?source=comment-gist)
**to join this conversation on GitHub**.
Already have an account?
[Sign in to comment](https://gist.github.com/login?return_to=https%3A%2F%2Fgist.github.com%2Fnk521%2Fc476c7fef884fed3226e6bc809a80e8c)

Footer
------

© 2026 GitHub, Inc.

### Footer navigation

* [Terms](https://docs.github.com/site-policy/github-terms/github-terms-of-service)
* [Privacy](https://docs.github.com/site-policy/privacy-policies/github-privacy-statement)
* [Security](https://github.com/security)
* [Status](https://www.githubstatus.com/)
* [Community](https://github.community/)
* [Docs](https://docs.github.com/)
* [Contact](https://support.github.com?tags=dotcom-footer)
* Manage cookies
* Do not share my personal information

You can’t perform that action at this time.
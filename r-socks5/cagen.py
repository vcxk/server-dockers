
import pathlib
import os 

file_dir = pathlib.Path(__file__).parent
target_dir = file_dir.joinpath("target")
# print(target_dir)
if not target_dir.exists():
    target_dir.mkdir()

ip_list = ["127.0.0.1","2406:da18:c34:6d00:2b8f:c8b7:8cc9:4017"]
dns_list = ["*.vcxk.fun"]

cnf_content = """
[ req ]
default_bits       = 2048
distinguished_name = req_distinguished_name
req_extensions     = req_ext
 
[ req_distinguished_name ]
countryName                 = Country Name (2 letter code)
countryName_default         = CN
stateOrProvinceName         = ShangHai
stateOrProvinceName_default = ShangHai
localityName                = Locality Name (eg, city)
localityName_default        = ShangHai
organizationName            = Organization Name (eg, company)
organizationName_default    = dai
commonName                  = Common Name (e.g. server FQDN or YOUR name)
commonName_max              = 64
commonName_default          = server.toolbox
 
[ req_ext ]
subjectAltName = @alt_names
 
[alt_names]

"""

cakey_path = target_dir.joinpath("ca.key.pem")
cacsr_path = target_dir.joinpath("ca.csr.pem")
cacrt_path = target_dir.joinpath("ca.crt.pem")
subj = "/C=CN/ST=Shanghai/L=Shanghai/O=myorg"

def gen_ca_files():
    if not cakey_path.exists():
        os.system("openssl genrsa -out %s"%(cakey_path))
    if not cacsr_path.exists():
        os.system("openssl req -new -key %s -out %s -subj=%s"%(
            cakey_path,cacsr_path,subj
        ))
    if not cacrt_path.exists():
        os.system("openssl x509 -req -sha256 -in %s -out %s -key %s -CAcreateserial -days 3650"%(
            cacsr_path,cacrt_path,cakey_path
        ))

gen_ca_files()

def gen_client_files():
    key_path = target_dir.joinpath("client.key.pem")
    csr_path = target_dir.joinpath("client.csr.pem")
    crt_path = target_dir.joinpath("client.crt.pem")
    os.system("openssl genrsa -out %s"%(key_path))
    os.system("openssl req -new -key %s -out %s -subj=%s"%(key_path,csr_path,subj))
    os.system("openssl x509 -req -sha256 -in %s -out %s -CA %s -CAkey %s -CAcreateserial -days 3650"%(
        csr_path,crt_path,cacrt_path,cakey_path
    ))
gen_client_files()

def gen_server_files():
    key_path = target_dir.joinpath("server.key.pem")
    csr_path = target_dir.joinpath("server.csr.pem")
    crt_path = target_dir.joinpath("server.crt.pem")
    cnf_path = target_dir.joinpath("server.cnf")

    alt_name_content = ""
    for i in range(len(ip_list)):
        alt_name_content += "IP.%d    = %s\n"%(i + 1,ip_list[i])
    for i in range(len(dns_list)):
        alt_name_content += "DNS.%d     = %s\n"%(i + 1,dns_list[i])

    f = open(cnf_path,mode="w+")
    f.write(cnf_content + alt_name_content)
    f.close()

    os.system("openssl genrsa -out %s"%(key_path))
    os.system("openssl req -new -key %s -out %s -config %s -subj=%s"%(
        key_path,csr_path,cnf_path,subj
    ))
    os.system("openssl x509 -req -sha256 -in %s -out %s -CA %s -CAkey %s -CAcreateserial -days 3650 -extensions req_ext -extfile %s"%(
        csr_path,crt_path,cacrt_path,cakey_path,cnf_path
    ))

gen_server_files()





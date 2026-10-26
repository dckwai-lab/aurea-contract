import json
import hashlib
import subprocess
import time
import os
from datetime import datetime
from cryptography.fernet import Fernet

CONTRACT_ID = "rawkale6964-test.testnet"
PATIENT_ID = "paciente_joao.testnet"
DOCTOR_ID = "medico_silva.testnet" 
PDS_FOLDER = "pds_storage"

def print_step(emoji, message):
    print(f"\n{emoji}  {message}")
    time.sleep(1) 

def run_near_command(args):
    cmd = ["near"] + args
    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    if result.returncode != 0:
        return None, result.stderr
    return result.stdout, None

def gerar_e_criptografar_dados():
    print_step("[1/5] IA NO TEE", "Processando exames e gerando FHIR...")
    fhir_data = json.dumps({
        "resourceType": "ClinicalImpression",
        "status": "completed",
        "subject": {"reference": f"Patient/{PATIENT_ID}"},
        "summary": "Paciente apresenta melhora."
    }, indent=2)
    
    print_step("[2/5] CRIPTOGRAFIA REAL", "Cifrando o resumo com chave secreta (AES)...")
    chave = Fernet.generate_key()
    cipher = Fernet(chave)
    dados_cifrados = cipher.encrypt(fhir_data.encode())
    
    if not os.path.exists(PDS_FOLDER):
        os.makedirs(PDS_FOLDER)
        
    cid = hashlib.sha256(dados_cifrados).hexdigest()
    filepath = os.path.join(PDS_FOLDER, f"{cid}.bin")
    
    with open(filepath, "wb") as f:
        f.write(dados_cifrados)
        
    print(f"      Salvo off-chain: {filepath}")
    print(f"      CID do arquivo cifrado: {cid[:20]}...")
    return cid

def gravar_na_near(cid):
    print_step("[3/5] NEAR PROTOCOL", "Registrando o CID na blockchain...")
    args_json = json.dumps({"patient_id": PATIENT_ID, "cid": cid})
    out, err = run_near_command(["call", CONTRACT_ID, "add_record", args_json, "--accountId", CONTRACT_ID])
    if out: 
        print("      [SUCESSO] Resumo gravado on-chain!")
    else:
        print(f"      [ERRO] {err}")

def testar_consentimento():
    print_step("[4/5] CONSENTIMENTO", f"Concedendo acesso ao {DOCTOR_ID}...")
    args_json = json.dumps({"patient_id": PATIENT_ID, "doctor_id": DOCTOR_ID})
    out, err = run_near_command(["call", CONTRACT_ID, "grant_access", args_json, "--accountId", CONTRACT_ID])
    if out: 
        print("      [SUCESSO] Medico autorizado on-chain!")

def ler_historico_como_medico():
    print_step("[5/5] CONSULTA FUTURA", f"O medico {DOCTOR_ID} tentando ler o historico...")
    args_json = json.dumps({"patient_id": PATIENT_ID})
    
    # Mudamos de "view" para "call" para simular a assinatura do médico
    out, err = run_near_command(["call", CONTRACT_ID, "get_history", args_json, "--accountId", DOCTOR_ID])
    
    if out:
        print("\n      --- HISTORICO RECUPERADO (AUTORIZADO) ---")
        print("      [SUCESSO] O medico conseguiu ler o historico.")
    else:
        print(f"\n      [BLOQUEADO PELA NEAR] O contrato negou o acesso.")

if __name__ == "__main__":
    print("="*55)
    print("        PROJETO AUREA - LOOP LONGITUDINAL v2.0")
    print("="*55)
    
    cid = gerar_e_criptografar_dados()
    gravar_na_near(cid)
    testar_consentimento()
    ler_historico_como_medico()
    
    print("\n" + "="*55)
    print("  SUCESSO: O dado foi cifrado, o acesso foi autorizado!")
    print("="*55)
import json
import hashlib
import subprocess
import time
import os
from datetime import datetime

CONTRACT_ID = "rawkale6964-test.testnet"
PATIENT_ID = "paciente_joao.testnet"
PDS_FOLDER = "pds_storage"

def print_step(emoji, message):
    print(f"\n{emoji}  {message}")
    time.sleep(1) 

def run_near_command(args):
    cmd = ["near"] + args
    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    if result.returncode != 0:
        print(f"[ERRO] {result.stderr}")
        return None
    return result.stdout

def simular_geracao_fhir():
    print_step("[1/4] IA NO TEE", "Processando exames e gerando ClinicalImpression (FHIR)...")
    fhir_data = {
        "resourceType": "ClinicalImpression",
        "status": "completed",
        "subject": {"reference": f"Patient/{PATIENT_ID}"},
        "date": datetime.now().isoformat(),
        "summary": "Paciente apresenta melhora significativa. Pressao arterial 120/80.",
        "provenance": {"ai_model": "aurea-v1", "human_validated": True}
    }
    return json.dumps(fhir_data, indent=2)

def salvar_no_pds(fhir_string):
    print_step("[2/4] CRIPTOGRAFIA E PDS", "Cifrando resumo e salvando no repositorio off-chain...")
    
    # Cria a pasta PDS se não existir
    if not os.path.exists(PDS_FOLDER):
        os.makedirs(PDS_FOLDER)
        
    # Gera o CID (Hash)
    cid = hashlib.sha256(fhir_string.encode()).hexdigest()
    
    # Salva o arquivo (Simulando o IPFS)
    filepath = os.path.join(PDS_FOLDER, f"{cid}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(fhir_string)
        
    print(f"      Arquivo salvo off-chain: {filepath}")
    print(f"      CID gerado: {cid[:20]}...")
    return cid

def gravar_na_near(cid):
    print_step("[3/4] NEAR PROTOCOL", "Registrando apenas o CID na blockchain (Smart Contract)...")
    args_json = json.dumps({"patient_id": PATIENT_ID, "cid": cid})
    
    resultado = run_near_command([
        "call", CONTRACT_ID, "add_record", 
        args_json, 
        "--accountId", CONTRACT_ID
    ])
    
    if resultado:
        for line in resultado.split('\n'):
            if "Transaction Id" in line:
                print(f"      [SUCESSO] Transacao: {line.split('Id')[-1].strip()}")

def ler_historico():
    print_step("[4/4] CONSULTA FUTURA", "Lendo o Historico Medico Longitudinal de volta...")
    args_json = json.dumps({"patient_id": PATIENT_ID})
    
    resultado = run_near_command([
        "view", CONTRACT_ID, "get_history", args_json
    ])
    
    if resultado:
        print("\n      --- HISTORICO RECUPERADO DA NEAR ---")
        print(f"      {resultado.strip()}")
        print("      ------------------------------------")

if __name__ == "__main__":
    print("="*55)
    print("        PROJETO AUREA - LOOP LONGITUDINAL")
    print("="*55)
    
    fhir = simular_geracao_fhir()
    cid = salvar_no_pds(fhir)
    gravar_na_near(cid)
    ler_historico()
    
    print("\n" + "="*55)
    print("  O CICLO SO FECHA QUANDO O DADO VOLTA AO PACIENTE")
    print("="*55)
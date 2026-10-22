import json
import hashlib
import subprocess
import time
from datetime import datetime

CONTRACT_ID = "rawkale6964-test.testnet"
PATIENT_ID = "paciente_joao.testnet"

def print_step(emoji, message):
    print(f"\n{emoji}  {message}")
    time.sleep(1) # Pausa dramática para o vídeo ficar bom

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
    return json.dumps(fhir_data)

def gerar_cid_simulado(fhir_string):
    print_step("[2/4] CRIPTOGRAFIA", "Cifrando resumo com a chave do paciente e gerando CID...")
    cid = hashlib.sha256(fhir_string.encode()).hexdigest()
    print(f"      CID gerado: {cid[:20]}... (IPFS simulado)")
    return cid

def gravar_na_near(cid):
    print_step("[3/4] NEAR PROTOCOL", "Registrando o indice na blockchain (Smart Contract)...")
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
                print("      [SUCESSO] Resumo gravado on-chain!")

def ler_historico():
    print_step("[4/4] CONSULTA FUTURA", "Lendo o Historico Medico Longitudinal de volta...")
    args_json = json.dumps({"patient_id": PATIENT_ID})
    
    resultado = run_near_command([
        "view", CONTRACT_ID, "get_history", args_json
    ])
    
    if resultado:
        print("\n      --- HISTORICO RECUPERADO DO PACIENTE ---")
        print(f"      {resultado.strip()}")
        print("      ----------------------------------------")

if __name__ == "__main__":
    print("="*50)
    print("        PROJETO AUREA - LOOP LONGITUDINAL")
    print("="*50)
    
    fhir = simular_geracao_fhir()
    cid = gerar_cid_simulado(fhir)
    gravar_na_near(cid)
    ler_historico()
    
    print("\n" + "="*50)
    print("  O CICLO SO FECHA QUANDO O DADO VOLTA AO PACIENTE")
    print("="*50)
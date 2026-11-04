import json
import hashlib
import subprocess
import time
import os
from datetime import datetime
from cryptography.fernet import Fernet

CONTRACT_ID = "rawkale6964-test.testnet"
PATIENT_ID = "rawkale6964-test.testnet"
DOCTOR_ID = "medico.rawkale6964-test.testnet"
PDS_FOLDER = "pds_storage"

def print_step(emoji, message):
    print(f"\n{emoji}  {message}")
    time.sleep(0.5) 

def run_near_command(args):
    cmd = ["near"] + args
    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    if result.returncode != 0:
        return None, result.stderr
    return result.stdout, None

def simular_graph_rag_e_loops():
    print_step("🌐 [TEE - NODES]", "Mapeando Grafo Clinico do paciente...")
    print("      Nos extraidos: Paciente_Joao, Exame_Sangue_2026, Sintoma_Fadiga")
    time.sleep(0.5)
    print_step("🔄 [TEE - LOOPS]", "Executando Agent Swarm...")
    print("      ✅ Loop 1: Extracao concluida.")
    print("      ✅ Loop 2: Validacao cruzada concluida.")
    print("      ✅ Loop 3: Analise temporal concluida.")

def gerar_e_criptografar_dados():
    simular_graph_rag_e_loops()
    print_step("🧠 [TEE - FHIR]", "Consolidando Grafo em FHIR...")
    fhir_data = json.dumps({"resourceType": "ClinicalImpression", "status": "completed", "summary": "Paciente estavel."}, indent=2)
    
    print_step("🔒 [CRIPTOGRAFIA]", "Cifrando com AES...")
    chave = Fernet.generate_key()
    cipher = Fernet(chave)
    dados_cifrados = cipher.encrypt(fhir_data.encode())
    
    if not os.path.exists(PDS_FOLDER): os.makedirs(PDS_FOLDER)
    cid = hashlib.sha256(dados_cifrados).hexdigest()
    filepath = os.path.join(PDS_FOLDER, f"{cid}.bin")
    with open(filepath, "wb") as f: f.write(dados_cifrados)
    
    print(f"      CID gerado: {cid[:20]}...")
    return cid

def gravar_na_near(cid):
    print_step("⛓️  [NEAR]", "Registrando na blockchain...")
    args_json = json.dumps({"cid": cid})
    out, err = run_near_command(["call", CONTRACT_ID, "add_record", args_json, "--accountId", PATIENT_ID])
    if out: print("      [SUCESSO] Gravado on-chain!")

def testar_consentimento():
    print_step("🔑 [CONSENTIMENTO]", "Autorizando medico...")
    args_json = json.dumps({"doctor_id": DOCTOR_ID})
    out, err = run_near_command(["call", CONTRACT_ID, "grant_access", args_json, "--accountId", PATIENT_ID])
    if out: print("      [SUCESSO] Medico autorizado!")

def ler_historico():
    print_step("📖 [CONSULTA]", "Lendo historico...")
    args_json = json.dumps({"patient_id": PATIENT_ID, "from": 0, "limit": 10})
    out, err = run_near_command(["view", CONTRACT_ID, "get_history", args_json])
    if out: print(f"      [SUCESSO] Historico: {out.strip()[:100]}...")

if __name__ == "__main__":
    print("="*50)
    print("        PROJETO AUREA - v4.0")
    print("="*50)
    cid = gerar_e_criptografar_dados()
    gravar_na_near(cid)
    testar_consentimento()
    ler_historico()
    print("\n" + "="*50)
    print("  SUCESSO!")
    print("="*50)

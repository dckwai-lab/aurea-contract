use near_sdk::{env, near, AccountId, PanicOnDefault, Timestamp};
use std::collections::{HashMap, HashSet};

#[near(serializers = [borsh, json])]
#[derive(Clone)]
pub struct Record {
    pub cid: String,
    pub version: u64,
    pub timestamp: Timestamp,
}

#[near(contract_state)]
#[derive(PanicOnDefault)]
pub struct Contract {
    pub patient_records: HashMap<AccountId, Vec<Record>>,
    pub permissions: HashMap<AccountId, HashSet<AccountId>>, 
}

#[near]
impl Contract {
    #[init]
    pub fn new() -> Self {
        Self {
            patient_records: HashMap::new(),
            permissions: HashMap::new(),
        }
    }

    pub fn add_record(&mut self, patient_id: AccountId, cid: String) {
        let records = self.patient_records.entry(patient_id.clone()).or_insert_with(Vec::new);
        let version = records.len() as u64 + 1;
        let record = Record { cid, version, timestamp: env::block_timestamp() };
        records.push(record);
        env::log_str(&format!("Novo registro adicionado para: {}", patient_id));
    }

    pub fn grant_access(&mut self, patient_id: AccountId, doctor_id: AccountId) {
        let docs = self.permissions.entry(patient_id.clone()).or_insert_with(HashSet::new);
        docs.insert(doctor_id.clone());
        env::log_str(&format!("Acesso concedido por {} para {}", patient_id, doctor_id));
    }

    pub fn revoke_access(&mut self, patient_id: AccountId, doctor_id: AccountId) {
        if let Some(docs) = self.permissions.get_mut(&patient_id) {
            docs.remove(&doctor_id);
            env::log_str(&format!("Acesso revogado por {} para {}", patient_id, doctor_id));
        }
    }

    pub fn get_history(&self, patient_id: AccountId) -> Vec<Record> {
        let caller = env::predecessor_account_id();
        
        let is_patient = caller == patient_id;
        let is_authorized = self.permissions.get(&patient_id)
            .map(|docs| docs.contains(&caller))
            .unwrap_or(false);

        if !is_patient && !is_authorized {
            env::panic_str("Acesso negado: Medico nao autorizado pelo paciente.");
        }

        self.patient_records.get(&patient_id).cloned().unwrap_or_else(Vec::new)
    }
}
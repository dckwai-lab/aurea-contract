use near_sdk::{env, near, AccountId, PanicOnDefault, Timestamp};
use std::collections::HashMap;

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
}

#[near]
impl Contract {
    #[init]
    pub fn new() -> Self {
        Self {
            patient_records: HashMap::new(),
        }
    }

    pub fn add_record(&mut self, patient_id: AccountId, cid: String) {
        let records = self.patient_records.entry(patient_id.clone()).or_insert_with(Vec::new);
        
        let version = records.len() as u64 + 1;
        let record = Record {
            cid,
            version,
            timestamp: env::block_timestamp(),
        };
        
        records.push(record);
        env::log_str(&format!("Novo registro adicionado para o paciente: {}", patient_id));
    }

    pub fn get_history(&self, patient_id: AccountId) -> Vec<Record> {
        self.patient_records.get(&patient_id).cloned().unwrap_or_else(Vec::new)
    }
}

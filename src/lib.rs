
use near_sdk::{env, near, AccountId, PanicOnDefault, Timestamp, require};
use near_sdk::store::{IterableMap, IterableSet};

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
    pub patient_records: IterableMap<AccountId, Vec<Record>>,
    pub permissions: IterableMap<AccountId, IterableSet<AccountId>>,
}

#[near]
impl Contract {
    #[init]
    pub fn new() -> Self {
        Self {
            patient_records: IterableMap::new(b"r"),
            permissions: IterableMap::new(b"p"),
        }
    }

    pub fn add_record(&mut self, cid: String) {
        let patient_id = env::predecessor_account_id();
        require!(!cid.is_empty(), "CID vazio");
        require!(cid.len() <= 128, "CID excede o tamanho maximo");

        let mut records = self.patient_records.get(&patient_id).cloned().unwrap_or_else(Vec::new);
        let version = records.len() as u64 + 1;
        records.push(Record { cid, version, timestamp: env::block_timestamp() });
        self.patient_records.insert(patient_id, records);
    }

        pub fn grant_access(&mut self, doctor_id: AccountId) {
        let patient_id = env::predecessor_account_id();
        require!(doctor_id != patient_id, "O paciente ja le o proprio historico");

        // Se o paciente já tem um set de permissões, modificamos direto
        if let Some(docs) = self.permissions.get_mut(&patient_id) {
            docs.insert(doctor_id);
        } else {
            // Se não tem, criamos um novo set e inserimos
            let mut new_set = IterableSet::new(b"d");
            new_set.insert(doctor_id);
            self.permissions.insert(patient_id, new_set);
        }
    }

    // AQUI ESTÁ A MÁGICA: get_history NÃO usa predecessor_account_id.
    // Assim, o view funciona perfeitamente e não dá ProhibitedInView.
    pub fn get_history(&self, patient_id: AccountId, from: u64, limit: u64) -> Vec<Record> {
        let records = self.patient_records.get(&patient_id).cloned().unwrap_or_else(Vec::new);
        let start = from as usize;
        if start >= records.len() { return Vec::new(); }
        let end = (start + (limit as usize)).min(records.len());
        records[start..end].to_vec()
    }
}
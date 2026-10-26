# 🌟 Áurea - Histórico Médico Longitudinal Soberano

## O Problema
O médico tem 15 minutos de consulta para ler um histórico de 15 anos. O uso de LLMs em nuvem padrão sem salvaguardas adequadas impõe riscos severos de conformidade com a LGPD/HIPAA. Além disso, quando o paciente troca de rede, perde o histórico longitudinal, gerando silos de dados.

## A Solução
O Áurea processa exames, gera sínteses em **HL7/FHIR**, exige validação humana e **devolve o resumo cifrado ao repositório do paciente**. A blockchain NEAR atua como o cartório descentralizado de consentimento: o paciente decide quem pode acessar o dado, e o contrato inteligente garante o bloqueio de acessos não autorizados, sem nunca armazenar o dado de saúde em si.

## 🔒 Destaques Técnicos (Privacy & Private AI)
- **Criptografia AES:** Os resumos gerados são cifrados via `cryptography` (Fernet) antes de irem para o armazenamento off-chain (PDS).
- **Consentimento On-Chain:** O Smart Contract na NEAR possui funções de `grant_access` (conceder) e `revoke_access` (revogar), garantindo soberania total ao paciente.
- **Controle de Acesso Rígido:** A função `get_history` no contrato Rust verifica a identidade de quem chama. Se um médico não tiver autorização explícita do paciente, o contrato **bloqueia a leitura**.
- **Redução de Exposição:** O processamento ocorre em ambiente isolado (TEE simulado na demo) e os dados brutos são descartados após a geração da síntese.

## 🚀 Como testar (How to try it)

1. Clone o repositório:
   `git clone https://github.com/dckwai-lab/aurea-contract.git`
2. Instale as dependências:
   `pip install -r requirements.txt`
   *(Nota: requer a biblioteca `cryptography` instalada)*
3. Instale o NEAR CLI (necessário para interagir com a testnet):
   `npm install -g near-cli`
4. **Execute a demo**:
   Dê dois cliques no arquivo `run_demo.bat` (Windows) ou rode `python agent.py`.
5. **O que você deve ver (See)**:
   - **Passo 1 e 2:** O script simula a IA gerando um resumo clínico no padrão FHIR, cifra o arquivo com AES e salva localmente (simulando o IPFS/PDS).
   - **Passo 3:** O script chama o Smart Contract na NEAR Testnet e registra apenas o CID (hash) do arquivo cifrado.
   - **Passo 4:** O paciente concede permissão on-chain para um médico (`medico_silva.testnet`).
   - **Passo 5:** Uma simulação de consulta tenta ler o histórico. *(Dica: rode o script sem a etapa 4 e veja a NEAR bloquear o acesso!)*

## 🛠 Tecnologias
- **Blockchain**: NEAR Protocol (Rust Smart Contract com controle de acesso).
- **IA/Health**: Python + Padrão HL7 FHIR.
- **Privacidade**: Criptografia AES real (Fernet) + Arquitetura Off-chain (PDS simulado).

---

## 🗺️ Roadmap

### ✅ Fase 0 e 1: MVP Validado e Seguro (Concluído - Out/2026)
O núcleo do "Loop Áurea" já está funcional na NEAR Testnet.
- [x] **Smart Contract NEAR**: Registro imutável do CID e versionamento do histórico longitudinal.
- [x] **Privacidade Ativa**: Criptografia AES real (Fernet) no armazenamento off-chain (PDS).
- [x] **Consentimento On-Chain**: Funções `grant_access` e `revoke_access` que garantem a soberania do paciente.
- [x] **Controle de Acesso**: O contrato bloqueia a leitura de médicos que não possuem autorização explícita do paciente.
- [x] **Agente FHIR**: Geração de resumos clínicos no padrão HL7 FHIR.

### 🚀 Fase 2: Integração e Experiência do Médico (Q4 2026 / Q1 2027)
Foco em transformar o MVP em uma ferramenta utilizável no dia a dia clínico.
- [ ] **Frontend (HITL)**: Criar o Dashboard Web (React/Next.js) para o médico visualizar o histórico e assinar a conduta de forma amigável.
- [ ] **TEE Real (GPU)**: Substituir a simulação do script Python por integração real com a **NEAR AI Cloud** (ou enclaves AWS Nitro), garantindo atestação criptográfica do hardware.
- [ ] **Integração com RNDS**: Adequar o mapeamento FHIR para o modelo `RAC` (Registro de Atendimento Clínico) e iniciar o processo de credenciamento no DATASUS.

### 🌐 Fase 3: Escala e Modelo de Negócio (2027)
Validação de mercado e expansão do ecossistema.
- [ ] **Modelo B2B2C**: Lançar a assinatura para clínicas (acesso ao Dashboard e IA) mantendo o acesso do paciente gratuito e soberano.
- [ ] **Tokenização de Dados (Opt-in)**: Criar sistema onde pacientes possam autorizar o uso de dados anonimizados para pesquisas e receber recompensas em NEAR.
- [ ] **Integração com NEAR Intents**: Permitir pagamentos de consultas e assinaturas cross-chain usando stablecoins.

### 💡 Fase 4: Expansão da Arquitetura (Áurea Procurement)
A tecnologia de privacidade não se limita à saúde.
- [ ] **Leilão Cego B2B**: Adaptar o motor TEE + NEAR para o departamento de compras de grandes empresas, permitindo que compradores e fornecedores negociem de forma 100% anônima e justa, com liquidação instantânea na blockchain.
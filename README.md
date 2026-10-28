# 🌟 Áurea - Histórico Médico Longitudinal Soberano

## 📌 O Problema
O médico tem 15 minutos de consulta para ler um histórico de 15 anos. O uso de LLMs em nuvem padrão sem salvaguardas adequadas impõe riscos severos de conformidade com a LGPD e o HIPAA. Além disso, quando o paciente troca de rede ou de médico, ele perde o acesso ao seu histórico longitudinal, gerando silos de dados, exames repetidos e decisões clínicas subótimas.

## 💡 A Solução
O Áurea é uma infraestrutura de inteligência clínica que processa exames, gera sínteses em **HL7/FHIR**, exige validação humana e **devolve o resumo cifrado ao repositório do paciente**. 

A blockchain **NEAR Protocol** atua como o cartório descentralizado de consentimento: o paciente decide quem pode acessar o dado, e o contrato inteligente garante o bloqueio de acessos não autorizados, sem nunca armazenar o dado de saúde on-chain.

## 🔒 Destaques Técnicos (Privacy & Private AI)

- **Graph RAG & Agent Swarms:** A arquitetura do TEE (Enclave Seguro) vai além do resumo linear. O motor extrai "nós" de um Grafo Clínico (sintomas, exames, medicamentos) e os processa em múltiplos loops paralelos de agentes, garantindo uma análise clínica profunda antes da geração do FHIR.
- **Criptografia AES Real:** Os resumos gerados são cifrados via `cryptography` (Fernet) antes de irem para o armazenamento off-chain (PDS - Personal Data Store).
- **Consentimento On-Chain:** O Smart Contract na NEAR possui funções de `grant_access` (conceder) e `revoke_access` (revogar), garantindo a soberania do paciente sobre seus dados.
- **Controle de Acesso Rígido:** A função `get_history` no contrato Rust verifica a identidade de quem chama. Se um médico não tiver autorização explícita do paciente, o contrato **bloqueia a leitura**.
- **Redução de Exposição:** O processamento ocorre em ambiente isolado (TEE simulado na demo). O roadmap inclui a implementação de atestação de hardware real e a gestão segura do ciclo de vida das chaves.

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
   - **Passo 1:** O TEE simula a extração de nós de um Grafo Clínico e roda múltiplos loops de análise (Agent Swarms).
   - **Passo 2:** O script gera um resumo clínico no padrão FHIR, cifra o arquivo com AES e salva localmente (simulando o IPFS/PDS).
   - **Passo 3:** O script chama o Smart Contract na NEAR Testnet e registra apenas o CID (hash) do arquivo cifrado.
   - **Passo 4:** O paciente concede permissão on-chain para um médico (`medico_silva.testnet`).
   - **Passo 5:** Uma simulação de consulta tenta ler o histórico. *(Dica: rode o script sem a etapa 4 e veja a NEAR bloquear o acesso!)*

## 🛠 Tecnologias
- **Blockchain**: NEAR Protocol (Rust Smart Contract com controle de acesso).
- **IA/Health**: Python + Padrão HL7 FHIR + Arquitetura de Grafos (Mock).
- **Privacidade**: Criptografia AES real (Fernet) + Arquitetura Off-chain (PDS simulado).

---

## 🗺️ Roadmap de Evolução

### ✅ Fase 1: MVP e Núcleo de Privacidade (Concluído - Out/2026)
O "Loop Áurea" está funcional na NEAR Testnet, resolvendo o problema de fragmentação com segurança.
- [x] **Smart Contract NEAR**: Registro imutável do CID e versionamento do histórico.
- [x] **Criptografia AES Real**: Resumos cifrados off-chain com a biblioteca Fernet.
- [x] **Consentimento On-Chain**: Funções `grant_access` e `revoke_access` no contrato.
- [x] **Controle de Acesso**: Bloqueio de leitura para médicos não autorizados pelo paciente.
- [x] **Agente Clínico (Simulado)**: Extração de nós (Graph RAG) e geração de FHIR com validação humana (HITL).

### 🚀 Fase 2: Confiabilidade Técnica e Clínica (Q1 2027)
Foco em transformar o MVP técnico em uma ferramenta clínica segura, auditável e utilizável.
- [ ] **TEE Real (Atestação)**: Migrar a simulação Python para a **NEAR AI Cloud** (ou enclaves AWS Nitro), garantindo isolamento criptográfico comprovado por hardware.
- [ ] **Gestão de Chaves (Social Recovery)**: Implementar a recuperação da chave do paciente via "guardiões" (contatos de confiança ou multisig), garantindo que a perda do dispositivo não signifique a perda do histórico médico.
- [ ] **Dashboard HITL (Frontend)**: Criar a interface em React/Next.js para o médico revisar, ajustar e assinar digitalmente as condutas (substituindo o terminal).
- [ ] **Prova de Conceito Auditável**: Criar suíte de testes com casos clínicos sintéticos para medir a taxa de omissões e a confiabilidade das sínteses.

### 🌐 Fase 3: Escala, RNDS e Modelo de Negócio (Q2 a Q4 2027)
Validação do modelo de negócios, custos de infraestrutura e integração com o ecossistema de saúde brasileiro.
- [ ] **Integração RNDS/DATASUS**: Adequar o mapeamento FHIR para o modelo RAC (Registro de Atendimento Clínico) e obter credenciamento.
- [ ] **Análise de Custo Unitário (ROI)**: Validar o custo total por consulta (inferência TEE + IA + armazenamento + NEAR) e comprovar a disposição a pagar das clínicas.
- [ ] **Modelo B2B2C**: Lançar assinatura para clínicas (acesso ao Dashboard e IA) mantendo o acesso do paciente gratuito e soberano.
- [ ] **Piloto Institucional**: Validar a adoção e a economia de tempo (ROI) em uma clínica ou hospital parceiro.

### 💡 Fase 4: Expansão de Arquitetura (2028+)
Uso da nossa infraestrutura de confiança em novos mercados.
- [ ] **Áurea Procurement (B2B)**: Adaptar o motor TEE + NEAR para leilões cegos no departamento de compras de grandes empresas, garantindo anonimato entre compradores e fornecedores.
- [ ] **Data-as-a-Service**: Sistema de opt-in onde pacientes autorizam o uso de dados anonimizados para pesquisas e recebem recompensas em NEAR (via NEAR Intents).
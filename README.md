# 🌟 Áurea - Histórico Médico Longitudinal Soberano

## O Problema
O médico tem 15 minutos de consulta para ler um histórico de 15 anos. Usar LLMs em nuvem para resumir prontuários viola LGPD/HIPAA, e quando o paciente troca de rede, perde o histórico.

## A Solução
O Áurea processa exames, gera sínteses em **HL7/FHIR**, exige validação humana e **devolve o resumo cifrado ao repositório do paciente**. A blockchain NEAR atua como o cartório descentralizado de consentimento: o paciente decide quem pode acessar o dado, e o contrato inteligente garante o bloqueio de acessos não autorizados, sem nunca armazenar o dado de saúde em si.

## 🔒 Destaques Técnicos (Privacy & Private AI)
- **Criptografia Real (AES):** Os resumos gerados são cifrados via `cryptography` (Fernet) antes de irem para o armazenamento off-chain (PDS).
- **Consentimento On-Chain:** O Smart Contract na NEAR possui funções de `grant_access` (conceder) e `revoke_access` (revogar), garantindo soberania total ao paciente.
- **Controle de Acesso Rígido:** A função `get_history` no contrato Rust verifica a identidade de quem chama. Se um médico não tiver autorização explícita do paciente, o contrato **bloqueia a leitura**.

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
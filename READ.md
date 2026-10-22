# 🌟 Áurea - Histórico Médico Longitudinal Soberano

## O Problema
O médico tem 15 minutos de consulta para ler um histórico de 15 anos. Usar LLMs em nuvem viola LGPD/HIPAA, e quando o paciente troca de rede, perde o histórico. 

## A Solução
O Áurea processa exames, gera sínteses em **HL7/FHIR**, exige validação humana e **devolve o resumo cifrado ao repositório do paciente** (na blockchain NEAR). O contrato na NEAR nunca guarda dados de saúde — apenas ponteiros (CIDs) e metadados.

## 🚀 Como testar (How to try it)

1. Clone o repositório:
   `git clone https://github.com/seu-usuario/aurea-contract.git`
2. Instale as dependências:
   `pip install -r requirements.txt`
3. Instale o NEAR CLI (necessário para interagir com a testnet):
   `npm install -g near-cli`
4. **Execute a demo**:
   Dê dois cliques no arquivo `run_demo.bat` (Windows) ou rode `python agent.py`.
5. **O que você deve ver (See)**:
   - O script vai simular a IA gerando um resumo clínico no padrão FHIR.
   - O script vai chamar o Smart Contract na NEAR Testnet.
   - O terminal mostrará o histórico do paciente sendo recuperado com a versão atualizada.

## 🛠 Tecnologias
- **Blockchain**: NEAR Protocol (Rust Smart Contract).
- **IA/Health**: Python + Padrão HL7 FHIR.
- **Privacidade**: Estrutura pronta para TEE e criptografia E2E (CIDs simulados na demo).
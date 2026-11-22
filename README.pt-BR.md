# Sniffer de Credenciais em Texto Claro

> 🇺🇸 [Read in English](README.md)

Um sniffer de rede construído com [Scapy](https://scapy.net/) para capturar e inspecionar tráfego em texto claro de protocolos inseguros (FTP, Telnet), desenvolvido como trabalho da disciplina de Redes de Computadores. Criado como exercício prático para entender por que protocolos de autenticação em texto claro são um risco de segurança.

## Por que este projeto

FTP e Telnet enviam credenciais em texto puro pela rede. Esta ferramenta demonstra esse risco capturando tráfego nas portas 21 (FTP) e 23 (Telnet), extraindo usuários e senhas, ofuscando as senhas capturadas na tela e classificando sua força usando entropia de Shannon.

## Status

**Funcional.** Captura e interpreta credenciais de FTP (comandos `USER`/`PASS`) e Telnet (reconstrução da sessão capturada caractere por caractere). As senhas são ofuscadas na saída do terminal e classificadas por força.

## Requisitos

- Python 3
- Privilégios de root (captura de pacotes brutos exige permissão elevada)
- Veja `requirements.txt` para as dependências Python

## Instalação

```bash
pip install -r requirements.txt
```

## Uso

```bash
sudo python3 sniffer.py
```

Execute em uma máquina posicionada para observar o tráfego FTP/Telnet (ex: na mesma rede host-only do alvo). Gere tráfego conectando a um servidor FTP ou Telnet enquanto o sniffer está rodando:

```bash
ftp <ip-do-alvo>
telnet <ip-do-alvo>
```

## Como funciona

- **FTP**: interpreta os comandos `USER`/`PASS` enviados como linhas de texto puro pelo cliente.
- **Telnet**: o protocolo envia dados caractere por caractere, então os caracteres são acumulados em um buffer até que um retorno de carro (`\r`) seja detectado, reconstruindo a linha completa. Os prompts `login:`/`Password:` enviados pelo servidor são usados para rastrear qual credencial (usuário ou senha) é esperada em seguida.
- **Ofuscação de senha**: apenas os 3 primeiros caracteres da senha capturada são exibidos; o restante é mascarado com `***`.
- **Cálculo de entropia**: a força da senha é estimada usando entropia de Shannon (distribuição de frequência dos caracteres). Os limites de classificação (`< 2` fraca, `2–3,5` média, `> 3,5` forte) foram definidos empiricamente para este exercício e não seguem um padrão oficial.

## Ambiente de teste (laboratório)

Testado contra o [Metasploitable2](https://sourceforge.net/projects/metasploitable/) em uma rede host-only isolada no VirtualBox, com uma VM Kali Linux como máquina atacante/de captura.

**⚠️ Uso educacional apenas em ambientes de laboratório controlados/isolados.** Não execute contra redes ou sistemas que você não possui ou não tem permissão explícita para testar.

## Limitações conhecidas

- **Ruído de negociação do Telnet**: a negociação de opções do protocolo Telnet (tipo de terminal, configurações de display, etc.) é marcada por um byte de controle (IAC, `0xFF`) que pode carregar texto literal e legível (ex: `XTERM-256COLOR`, `DISPLAY`) como parte do seu payload. Como esse texto é tecnicamente imprimível, ele não é filtrado pela checagem de caracteres imprimíveis atual, podendo aparecer misturado na linha de usuário capturada. Uma correção adequada exigiria detectar e remover as sequências de negociação prefixadas por IAC do payload bruto antes de reconstruir as linhas — isso foi identificado mas não implementado por restrição de tempo.

## Roadmap

- [x] Captura básica de pacotes nas portas 21/23
- [x] Extração de usuário/senha do FTP a partir dos comandos `USER`/`PASS`
- [x] Reconstrução e interpretação do stream caractere por caractere do Telnet
- [x] Ofuscação das senhas capturadas na saída do terminal
- [x] Cálculo e classificação da entropia da senha
- [ ] Remover as sequências de negociação IAC do Telnet do texto capturado (ver Limitações conhecidas)

## Aviso

Este projeto foi desenvolvido para um trabalho da disciplina de Redes de Computadores na universidade, apenas para fins educacionais.
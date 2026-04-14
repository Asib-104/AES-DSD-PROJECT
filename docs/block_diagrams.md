# AES-128 Hardware Architecture & Block Diagrams

The following diagrams illustrate the internal hardware architecture of the AES-128 core and how it interfaces with the physical Basys 3 board components via the UART wrapper.

## 1. System-Level Hardware Architecture (`uart_aes_top`)

This diagram shows how the computer communicates with the FPGA over USB-Serial, and how the top-level FSM buffers the 64 incoming characters, drives the AES core, and transmits the resulting ciphertext back.

```mermaid
graph TD
    subgraph PC["Computer / PuTTY Terminal"]
        TX_PC("UART TX (115200 baud)")
        RX_PC("UART RX (115200 baud)")
    end

    subgraph Basys3["Basys 3 FPGA Board"]
        Switch["Switch 0 (Decrypt Mode)"]
        Reset["Center Button (Reset)"]
        
        subgraph TopModule["uart_aes_top"]
            UART_RX["uart_rx"]
            UART_TX["uart_tx"]
            ControlFSM["Top-Level Buffer & Control FSM"]
            
            subgraph AESCore["aes_top (128-bit Datapath)"]
                CU["aes_control_unit"]
                AESLogic["AES Encryption & Decryption Datapaths"]
            end
        end
    end

    TX_PC -- Serial bitstream --> UART_RX
    UART_RX -- byte blocks --> ControlFSM
    
    Switch -- "decrypt=1/0" --> AESCore
    Reset -- "rst" --> ControlFSM
    Reset -- "rst" --> AESCore
    
    ControlFSM -- "plaintext (128-bit), key (128-bit), start" --> AESCore
    AESCore -- "done flow" --> ControlFSM
    AESCore -- "ciphertext (128-bit)" --> ControlFSM
    
    ControlFSM -- byte blocks --> UART_TX
    UART_TX -- Serial bitstream --> RX_PC
    
    classDef default fill:#f9f9f9,stroke:#333,stroke-width:1px;
    classDef highlight fill:#d4e6f1,stroke:#2874a6,stroke-width:2px;
    class AESCore highlight;
```

---

## 2. AES Core Iterative Datapath (`aes_top`)

To save valuable logic gates (LUTs) on the FPGA, this AES core uses an **iterative architecture**. Instead of unrolling 10 physical rounds of logic, one single hardware round is instantiated and the data is fed back into a 128-bit state register repeatedly for 10 clock cycles.

```mermaid
graph TD
    classDef reg_class fill:#fcf3cf,stroke:#b7950b,stroke-width:2px;
    classDef logic fill:#d5f5e3,stroke:#239b56,stroke-width:1px;
    classDef mux fill:#fadbd8,stroke:#b03a2e,stroke-width:2px;

    Key["cipher_key (128-bit)"] --> KEX("key_expansion"):::logic
    
    KEX -->|"rk0 .. rk10"| KeyMux{"Round Key Multiplexer"}:::mux
    RoundCounter["round_counter (0 to 10)"] --> KeyMux
    DecryptMode["decrypt mode signal"] --> KeyMux
    
    DataIn["plaintext (128-bit)"] --> InitXOR("Initial AddRoundKey"):::logic
    KeyMux -->|"current_round_key"| InitXOR
    
    InitXOR --> StateReg("128-bit State Register"):::reg_class
    
    StateReg --> EncLogic("aes_round"):::logic
    StateReg --> DecLogic("aes_inv_round"):::logic
    
    KeyMux --> EncLogic
    KeyMux --> DecLogic
    
    EncLogic --> MUX{"Encrypt/Decrypt Select"}:::mux
    DecLogic --> MUX
    DecryptMode --> MUX
    
    MUX -->|"128-bit round output"| StateReg
    
    StateReg -.->|"After cycle 10"| CipherOut["ciphertext output"]
```

---

## 3. Combinatorial Round Submodules

A single AES encryption/decryption round consists of four completely unclocked (combinatorial) mathematical transformations that execute continuously between clock edges.

```mermaid
graph LR
    classDef op fill:#ebdef0,stroke:#76448a,stroke-width:1px;

    subgraph EncryptRound["aes_round (Forward Cipher)"]
        direction LR
        in1["state_in"] --> SB("sub_bytes"):::op
        SB --> SR("shift_rows"):::op
        SR --> MC("mix_columns"):::op
        MC --> ARK("add_round_key"):::op
        rk1["round_key"] --> ARK
        ARK --> out1["state_out"]
    end

    subgraph DecryptRound["aes_inv_round (Inverse Cipher)"]
        direction LR
        in2["state_in"] --> ISR("inv_shift_rows"):::op
        ISR --> ISB("inv_sub_bytes"):::op
        ISB --> IARK("add_round_key"):::op
        rk2["round_key"] --> IARK
        IARK --> IMC("inv_mix_columns"):::op
        IMC --> out2["state_out"]
    end
```

### Note on Inverse Key Schedule
In the standard inverse cipher flow illustrated above, the key is dynamically indexed in reverse during operation (i.e. round 1 uses `rk[9]`, round 10 uses `rk[0]`). Because the `key_expansion` immediately calculates all 11 keys continuously in real-time, no extra clock cycles are wasted waiting for a backwards key expansion process.

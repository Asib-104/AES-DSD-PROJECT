# AES-128 FPGA Hardware Demonstration Guide

This guide outlines exactly how to demonstrate your AES-128 FPGA hardware integration to your professor or instructor using a Basys 3 board. It proves that your design not only simulates correctly but also processes data physically in real-time hardware.

## Phase 1: Programming the Board

Because you've integrated a UART interface, your top module is now `uart_aes_top`. First, burn the project onto the FPGA:

1. **Pull the Latest Code**: Make sure the Windows machine connected to the board has pulled the latest code from GitHub (which contains the UART and XDC files).
2. **Open Vivado**: Open `AES-DSD-PROJECT.xpr`.
3. **Generate Bitstream**: Click **Generate Bitstream** in the Flow Navigator. Wait for the synthesis, implementation, and bitstream generation to complete.
4. **Connect Hardware**: Plug in the Basys 3 board to the computer via USB and turn on the power switch.
5. **Program**: Click **Open Hardware Manager** > **Open Target** > **Auto Connect**. Finally, click **Program Device**. 

The "DONE" LED on the board should light up green, indicating your logic is loaded.

---

## Phase 2: Terminal Setup

Your FPGA acts as a serial device that receives keys/text and returns encrypted text.

1. **Find the COM Port**: Open "Device Manager" in Windows and expand **Ports (COM & LPT)**. Note the COM port number (e.g., `COM3`) next to "USB Serial Port."
2. **Open a Serial Terminal**: Open **Tera Term**, **PuTTY**, or the Arduino IDE Serial Monitor.
3. **Configure the Connection**:
   - **Port**: Select the COM port from step 1.
   - **Baud Rate**: **115200**
   - **Data bits**: **8**
   - **Stop bits**: **1**
   - **Parity**: **None**

*Note: Our hardware automatically ignores spaces and newlines, so line-ending settings in your terminal do not matter.*

---

## Phase 3: The Live Demo Execution

Once connected, your FPGA is actively waiting for input. You can identify the state of the hardware in real time via the onboard LEDs above the switches.

### Status LEDs Guide
*   💡 **LED 15 (Right-most, LED[0])**: ON = Constantly listening for UART data.
*   💡 **LED 14 (LED[1])**: ON = Computing AES cipher. *(Flashes too fast to easily see with the human eye!)*
*   💡 **LED 13 (LED[2])**: ON = Transmitting the 128-bit ciphertext back over UART.

### Sending the Test Vector

Explain to your teacher that you are feeding it official NIST standard test vectors. Send them the 64-character payload: the first 32 characters are the **Key**, and the next 32 are the **Plaintext**.

**Copy and paste the following string directly into the terminal window:**
```text
2B7E151628AED2A6ABF7158809CF4F3C3243F6A8885A308D313198A2E0370734
```

### The Expected Result

Instantly, the FPGA receives the ASCII text, parses it, computes the AES-128 cryptographic rounds in 12 hardware clock cycles, converts it back to ASCII via the UART TX module, and prints this response in your terminal:
```text
3925841D02DC09FBDC118597196A0B32
```

This perfectly matches the **FIPS-197 Appendix B** standard AES test vector, visually proving to your teacher that your combinational logic and hardware pathways are perfectly intact.

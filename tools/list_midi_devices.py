import mido

def list_midi_ports():
    print("\n=== AVAILABLE MIDI INPUT PORTS ===")
    for i, port in enumerate(mido.get_input_names()):
        print(f"[{i}] {port}")

    print("\n=== AVAILABLE MIDI OUTPUT PORTS ===")
    for i, port in enumerate(mido.get_output_names()):
        print(f"[{i}] {port}")

if __name__ == "__main__":
    print("Scanning for MIDI devices...\n")
    list_midi_ports()

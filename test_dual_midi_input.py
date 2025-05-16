import mido
import time

def find_port(name_fragment, inputs=True):
    names = mido.get_input_names() if inputs else mido.get_output_names()
    for name in names:
        if name_fragment in name:
            return name
    return None

# Identify ports
axiom_port = find_port("Axiom 25 MIDI In 0", inputs=True)
yamaha_port = find_port("Axiom 25 Ext MIDI In 1", inputs=True)
output_port = find_port("Microsoft GS Wavetable Synth", inputs=False)

if not axiom_port:
    print("❌ Axiom 25 MIDI In 0 not found.")
if not yamaha_port:
    print("❌ Axiom 25 Ext MIDI In 1 (Yamaha DIN) not found.")
if not output_port:
    print("❌ Microsoft GS Wavetable Synth not found.")

if axiom_port and yamaha_port and output_port:
    print(f"✅ Routing:\n - Axiom In:  {axiom_port}\n - Yamaha In: {yamaha_port}\n - Output:    {output_port}")
    
    with mido.open_output(output_port) as out, \
         mido.open_input(axiom_port) as axiom_in, \
         mido.open_input(yamaha_port) as yamaha_in:

        print("🎹 Now listening for input from both devices... Press Ctrl+C to stop.")
        while True:
            for msg in axiom_in.iter_pending():
                if not msg.is_meta:
                    out.send(msg)

            for msg in yamaha_in.iter_pending():
                if not msg.is_meta:
                    out.send(msg)

            time.sleep(0.01)
else:
    print("🛑 One or more required ports not available. Check connections.")


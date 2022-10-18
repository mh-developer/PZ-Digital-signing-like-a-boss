import time
import PySimpleGUI as sg
import hashlib
from Crypto.PublicKey import RSA

keyPair = RSA.generate(bits=2048)
print(f"Public key:  (n={hex(keyPair.n)}, e={hex(keyPair.e)})")
print(f"Private key: (n={hex(keyPair.n)}, d={hex(keyPair.d)})")


class DigitalSigning:
    def sign(self, message):
        message_digest = int(hashlib.sha256(message).hexdigest(), 16)
        print('Message Digest:', message_digest)

        digital_signature = pow(message_digest, keyPair.d, keyPair.n)
        print('Digital Signature:', digital_signature)
        return digital_signature

    def verify(self, message, signature):
        message_digest = int(hashlib.sha256(message).hexdigest(), 16)
        print('Message Digest:', message_digest)

        computed_message_digest = pow(signature, keyPair.e, keyPair.n)
        print('Computed Message Digest (From Signature)', computed_message_digest)

        if message_digest == computed_message_digest:
            return True
        return False


def start_gui():
    layout = [
        [sg.Text('Datoteka'), sg.InputText(key='_file_input_'), sg.FileBrowse('Odpri')],
        [sg.Output(size=(88, 22))],
        [
            sg.Button(button_text='Podpiši', key='_sign_button_'),
            sg.Button(button_text='Preveri', key='_verify_button_'),
            sg.Cancel(button_text='Zapri', key='_close_button_')
        ]
    ]
    window = sg.Window('Digital signing', layout)

    while True:
        event, values = window.read()
        if event in (None, 'Exit', 'Cancel', 'Zapri', '_close_button_'):
            break

        if event == '_sign_button_' or event == '_verify_button_':
            filepath = is_validation_ok = None
            filepath = values['_file_input_']

            try:
                print("------------------------------------------------")
                start_time = time.process_time()

                with open(filepath, 'rb') as data:
                    file = data.read()

                signing = DigitalSigning()

                if event == '_sign_button_':
                    print(f"---- INPUTS file: {filepath}")
                    print("OUTPUT: ")
                    signature = signing.sign(file)
                    print("------------------------------------------------")
                    print("------------------------------------------------")
                    print("VERIFY OUTPUT: ")
                    signature_verify = signing.verify(file, signature)
                    print("Is verified?", signature_verify)
                    print("--- End Signing ---")

                elif event == '_verify_button_':
                    pass

                print("------------------------------------------------")

            except:
                print('*** Napaka v procesu hashiranja ***')
    window.close()


if __name__ == '__main__':
    start_gui()

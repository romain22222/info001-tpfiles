import socket
import ssl

# Paramètres du client
HOST = 'www.negro.fr'
PORT = 12345
ROOT_CERT_FILE = './certsAndKeys/root-ca-lorne.pem'

# Création du socket client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Établir la connexion sécurisée avec TLS
ssl_socket = ssl.wrap_socket(client_socket, ca_certs=ROOT_CERT_FILE, cert_reqs=ssl.CERT_REQUIRED)
ssl_socket.connect((HOST, PORT))

# Récupère le certificat du serveur et fait les checks préliminaires (vérification de la signature et date d'expiration)
server_cert = ssl_socket.getpeercert()
# Vérifie si le domaine demandé est dans la liste des domaines certifié par le certificat. Si c'est pas le cas : erreur.
names = [v[0][1] for v in server_cert['subject'] if v[0][0] == 'commonName'] + [v[1] for v in server_cert['subjectAltName']]
if HOST not in names:
    raise ValueError(f"Le domaine du certificat ({names}) ne correspond pas au domaine attendu ({HOST})")

print(f"Connexion sécurisée établie avec {HOST}:{PORT}")
# Envoyer des messages au serveur
while True:
    message = input("Saisissez un message (ou 'exit' pour quitter) : ")
    ssl_socket.sendall(message.encode('utf-8'))
    if message.lower() == 'exit':
        break

# Fermer la connexion
ssl_socket.close()
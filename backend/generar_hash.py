from werkzeug.security import generate_password_hash

contraseña = input("Sereunhackerenelfuturo: ")
hash_generado = generate_password_hash(contraseña)
print("Tu hash es:")
print(hash_generado)

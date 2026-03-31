import random

# Probabilidades base
p_defectuosa = 0.04
p_no_defectuosa = 1 - p_defectuosa

# 1. Cálculo teórico
p_DD = p_defectuosa * p_defectuosa
p_DN = p_defectuosa * p_no_defectuosa
p_ND = p_no_defectuosa * p_defectuosa
p_NN = p_no_defectuosa * p_no_defectuosa

print("=== Cálculo teórico ===")
print(f"P(D,D) (ambas defectuosas): {p_DD:.4f}")
print(f"P(N,N) (ninguna defectuosa): {p_NN:.4f}")
p_al_menos_una = 1 - p_NN
print(f"P(al menos una defectuosa): {p_al_menos_una:.4f}")

# 2. Simulación (Monte Carlo)
num_experimentos = 100000
cont_DD = 0
cont_NN = 0
cont_al_menos_una = 0

for _ in range(num_experimentos):
    # Simulamos 2 lámparas
    # 1 = defectuosa, 0 = no defectuosa
    lampara1 = 1 if random.random() < p_defectuosa else 0
    lampara2 = 1 if random.random() < p_defectuosa else 0

    if lampara1 == 1 and lampara2 == 1:
        cont_DD += 1
    if lampara1 == 0 and lampara2 == 0:
        cont_NN += 1
    if lampara1 == 1 or lampara2 == 1:
        cont_al_menos_una += 1

print("\n=== Simulación ===")
print(f"P(D,D) simulada: {cont_DD / num_experimentos:.4f}")
print(f"P(N,N) simulada: {cont_NN / num_experimentos:.4f}")
print(f"P(al menos una D) simulada: {cont_al_menos_una / num_experimentos:.4f}")

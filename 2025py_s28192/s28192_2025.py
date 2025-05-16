# Cel programu:
# Generator losowej sekwencji DNA w formacie FASTA z dodatkowymi statystykami
# oraz możliwością osadzenia imienia użytkownika w sekwencji (bez wpływu na długość i statystyki).

# Kontekst:
# Program znajduje zastosowanie w bioinformatyce jako generator danych testowych do analizy genetycznej.

import random
# ORIGINAL:
# sequence = ''.join(random.choices('ACGT', k=length))  # Generowanie ciągu z liter A, C, G, T

# MODIFIED (lepsza czytelność i możliwość wielokrotnego użycia):
def generate_dna_sequence(length):
    """
    Generuje losową sekwencję DNA o zadanej długości.
    """
    nucleotides = ['A', 'C', 'G', 'T']
    return ''.join(random.choices(nucleotides, k=length))


# --- Funkcja do wstawiania imienia --- #

# ORIGINAL:
# position = random.randint(0, len(sequence))
# final_sequence = sequence[:position] + name + sequence[position:]

# MODIFIED (przeniesienie do funkcji, czytelność):
def insert_name(sequence, name):
    """
    Wstawia imię użytkownika w losowe miejsce sekwencji DNA.
    """
    position = random.randint(0, len(sequence))
    return sequence[:position] + name + sequence[position:]


# --- Funkcja do liczenia statystyk --- #

# ORIGINAL:
# stats = {n: sequence.count(n)/len(sequence) for n in 'ACGT'}
# cg_percent = (stats['C'] + stats['G']) * 100

# MODIFIED (usunięcie wpływu imienia na statystyki, zaokrąglenia, czytelność):
def calculate_stats(sequence):
    """
    Oblicza procentową zawartość nukleotydów A, C, G, T oraz %CG.
    Imię jest pomijane przy obliczeniach.
    """
    clean_sequence = ''.join(filter(lambda x: x in 'ACGT', sequence))  # Ignorujemy znaki spoza DNA
    total = len(clean_sequence)
    stats = {n: round((clean_sequence.count(n) / total) * 100, 1) for n in 'ACGT'}
    cg_percent = round(stats['C'] + stats['G'], 1)
    return stats, cg_percent


# --- Pobieranie danych od użytkownika --- #

length = int(input("Podaj długość sekwencji: "))          # Zapytanie o długość
seq_id = input("Podaj ID sekwencji: ")                    # Zapytanie o ID
description = input("Podaj opis sekwencji: ")             # Zapytanie o opis
name = input("Podaj imię: ")                              # Zapytanie o imię


# --- Generowanie i modyfikacja sekwencji --- #

original_sequence = generate_dna_sequence(length)
final_sequence = insert_name(original_sequence, name)

# --- Zapis do pliku FASTA --- #

filename = f"{seq_id}.fasta"

# ORIGINAL:
# with open(filename, "w") as fasta_file:
#     fasta_file.write(f">{seq_id} {description}\n{final_sequence}")

# MODIFIED (czytelniejszy zapis + zgodność z FASTA: nagłówek i sekwencja osobno):
with open(filename, "w") as fasta_file:
    fasta_file.write(f">{seq_id} {description}\n")
    fasta_file.write(final_sequence + "\n")

print(f"Sekwencja została zapisana do pliku {filename}")

# --- Obliczanie i wyświetlanie statystyk --- #

stats, cg_ratio = calculate_stats(final_sequence)

print("Statystyki sekwencji:")
for nucleotide in 'ACGT':
    print(f"{nucleotide}: {stats[nucleotide]}%")
print(f"%CG: {cg_ratio}%")
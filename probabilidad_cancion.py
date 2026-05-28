import math
letra_cancion = """

Find your dreams come true
And I wonder if you know
What it means what it means
And I wonder if you know
What it means what it means
And I wonder if you know
What it means to find your dreams
And I wonder

I hav been waiting on this my whole life
And I wonder
These dreams be waking me up at night
And I wonder
You say I think I am never wrong
And I wonder
You know what Maybe you are right aight

And I wonder if you know
What it means what it means
And I wonder if you know
What it means to find your dreams
And I wonder
You say he get on your fucking nerves
And I wonder
You hope that he get what he deserves word
And I wonder
Do you even remember what the issue is
You just trying to find where the tissue is
You can still be who you wish you is
It ai not happen yet and that is what intuition is and I wonder

When you hop back in the car
Drive back to the crib run back to they arms
The smokescreens the chokes and the screams
You ever wonder what it all really means

And I wonder if you know
What it means what it means
And I wonder if you know
What it means to find your dreams
And I wonder

And I am back on my grind
A psychic read my lifeline told me in my lifetime
My name would help light up the Chicago skyline
And that is why I am and I wonder
Seven o clock that is primetime
Heaven all watch God calling from the hotlines
Why he keep giving me hot lines
I am a star how could I not shine And I wonder

How many ladies in the house If you know
How many ladies in the house without a spouse What it means
Something in your blouse got me feeling so aroused what it means
What you about And I wonder

On that independent if you know
Trade it all for a husband and some kids what it means
You ever wonder what it all really mean
You wonder if you will ever find your dreams To find your dreams come true"""

def funcion_repeticion():
    
    cancion_minusculas = letra_cancion.lower() 
    repeticiones = {}
    total_letras = 0
    for letra in cancion_minusculas:

        if letra == " " or letra == "\n":
            continue  
        
        if letra in repeticiones:
            repeticiones[letra] += 1
        else:
            repeticiones[letra] = 1

        total_letras += 1
    return repeticiones, total_letras

diccionario_letras, conteo_total = funcion_repeticion()
print(f"Total de letras: {conteo_total}")

def calcular_entropia_y_probabilidades(repeticiones, total_letras):
    entropia_total = 0
    probabilidades = {}
    
    print("RESULTADOS")
    print(f"{'Letra':<6}  {'Conteo':<8}  {'Probabilidad':<18}  {'Bits/letra ':<24}")
    
    letras_ordenadas = sorted(repeticiones.items(), key=lambda item: item[1], reverse=True)
    
    for letra, conteo in letras_ordenadas:
        
        p_x = conteo / total_letras
        probabilidades[letra] = p_x
        
        bits_xLetra = -math.log2(p_x) 
        
        aporte_entropia = p_x * bits_xLetra
        entropia_total += aporte_entropia

        bits_redondeados = int(round(bits_xLetra))
        
        print(f"  {letra:<4}  {conteo:<8}  {(p_x * 100):<5.2f}{'%':<16}  {bits_redondeados:<16}")
        
    print(f"ENTROPIA TOTAL: {entropia_total:.0f} bits/letra")
    
    return probabilidades, entropia_total

probabilidades_cancion, entropia_final = calcular_entropia_y_probabilidades(diccionario_letras, conteo_total)
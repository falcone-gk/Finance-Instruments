# Finance-Instruments
Básica librería de instrumentos financieros, usado para resolver ejercicios.

## Prerrequsitos
El código está en Python 3 y se necesitan de las siguiente librerías.

- numpy
- matplotlib

## Instalación
Para poder usar el código es necesario que ubique el archivo **pynance.py** en el mismo folder de su proyecto y de allí importarlo, de igual manera para correr el archivo **test.py**.

## Explicación
El motivo de este proyecto es el de resolver ejercicios básicos de bonos y portafolios (en desarrollo).

### Bonos
En los bonos lo que se ha desarrollado es la obtención del **precio del bono** conociendo su Valor Nominal, tasa de interés, tasa cupón y tiempo del ejercicio. El precio se obtiene con la siguiente fórmula:

![equation](https://latex.codecogs.com/gif.latex?P%20%3D%20%5Csum_%7Bi%3D1%7D%5En%20%5Cfrac%7BC%7D%7B%281&plus;r%29%5En%7D%20&plus;%20%5Cfrac%7BVN%7D%7B%281&plus;r%29%5En%7D)

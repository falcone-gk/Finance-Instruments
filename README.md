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

![equations](https://latex.codecogs.com/png.latex?P%20%3D%20%5Csum_%7Bi%3D1%7D%5En%20%5Cfrac%7BC%7D%7B%281&plus;r%29%5En%7D%20&plus;%20%5Cfrac%7BVN%7D%7B%281&plus;r%29%5En%7D)

La duración del bono (duración de macaulay), se obtiene de la siguiente fórmula:

![equations](https://latex.codecogs.com/gif.latex?D%20%3D%20%5Cfrac%7B1%7D%7BP%7D%5Cleft%28%5Csum_%7Bt%3D1%7D%5En%20t%20%5Cfrac%7BC_t%7D%7B%281&plus;i%29%5Et%7D%20&plus;%20%5Cfrac%7Bn%20%5Ctimes%20VN%7D%7B%281&plus;i%29%5En%7D%5Cright%29)

La duración modificada resulta de la duración de macaulay:

![equations](https://latex.codecogs.com/gif.latex?DM%20%3D%20%5Cfrac%7BD%7D%7B%281&plus;i%29%7D)

La convexidad se obtiene de la siguiente fórmula:

![equations](https://latex.codecogs.com/gif.latex?Conv%20%3D%20%5Cfrac%7B1%7D%7BP%7D%5Cleft%28%5Csum_%7Bt%3D1%7D%5En%20%5Cfrac%7Bt%28t&plus;1%29C_t%7D%7B%281&plus;i%29%5E2%7D%20&plus;%20%5Cfrac%7Bn%28n&plus;1%29VN%29%7D%7B%281&plus;i%29%5E%7Bn&plus;2%7D%7D%20%5Cright%20%29)

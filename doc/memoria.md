---
title: |
    | boost.python
subtitle: |
    | Programación Técnica y Científica
    |
 	| Iván Garzón Segura
	| Práxedes Martínez Moreno
	| Vladislav Nikolov
	| 
	| 
titlepage: true
toc: true # Añadir índice
toc-own-page: true
lang: es-ES
listings-no-page-break: true
listings-disable-line-numbers: true
logo: logoUGR.jpg
logo-width: 175
---

# Introducción

Como bien sabemos, python es un lenguaje interpretado. Esto tiene ciertas ventajas e inconvenientes, siendo uno de dichos inconvenientes la velocidad a la hora de realizar grandes cantidades de cómputo, algo en lo que justamente destacan los lenguajes compilados.  

El objetivo de este trabajo es presentar una herramienta que nos permite combinar ambos tipos de lenguajes con el fin de aprovechar las ventajas de cada uno de ellos. Esta herramienta es *boost.python*, la cual emplearemos para introducir en python módulos que fueron previamente compilados en C++.  
Para comprender el funcionamiento de *boost.python* se expondrá un ejemplo sencillo de clases en C++ y, para comparar las diferencias entre usar esta herramienta y no hacerlo, recurriremos a un ejemplo más complejo basado en la *supresión de no máximos* usada en Visión Computador para extraer regiones relevantes de una imagen. 

# Boost Python

La biblioteca Boost Python nos permite crear módulos en C++, sin usar otras herramientas que no sean un editor y su respectivo compilador, que podremos importar desde Python. En estos módulos creados podremos exponer tanto clases y funciones, como objetos que podrán ser utilizados posteriormente en cualquier *script* de Python en los cuales este módulo sea importado. Uno de los objetivos de esta biblioteca es ser mínimamente intrusivo en el diseño del código en C++. 

Para comprender mejor el funcionamiento de esta herramienta, a continuación se exponen dos ejemplos, uno básico y otro más complejo. 

## Ejemplo básico

> Podemos encontrar el código de este ejemplo en el directorio *basicExamples* y contenido en los archivos *basic.cpp* y *basic.py*.

Para comenzar vamos a ver un ejemplo detallado con el fin de comprender cómo se exponen funciones de C++ a Python. 

En primer lugar, empecemos con el en el código en C++. Tenemos que importar la biblioteca de *boost.python*, además de aquellas otras que vayamos a necesitar:   

```cpp
#include <boost/python.hpp>
#include <string>
#include <cmath>
```

A continuación procederíamos a implementar las distintas funciones que luego emplearemos en el *script* de Python. Un ejemplo de función podría ser el siguiente:

```cpp
template <typename T>
T genericSum(T a, T b)
{
    return a + b;
}
```

Como podemos observar, esta función simplemente calcula la suma de dos valores de un tipo genérico y la retorna. Para poder usarla en Python, hemos de crear un módulo de *Boost.Python* y, posteriormente, exponerla en el mismo. Para hacer esto último, tenemos que indicar:

```cpp
BOOST_PYTHON_MODULE(basic)
{
    using namespace boost::python;

    // Expose generic function
    def("generic_sum", genericSum<int>);
    def("generic_sum", genericSum<float>);
    def("generic_sum", genericSum<std::string>);
}
```

En la primera línea de este fragmento de código se declara el módulo de *Boost.Python* que se importará desde Python posteriormente con el nombre que queremos asignarle, que en este caso es *basic*. A continuación, dentro de dicho módulo definimos el namespace que usa *Boost.Python* y exponemos la función definida previamente haciendo uso de ```def(<nombre de la función en Python>, <función en C++>)``` por cada uno de los tipos de dato a los que queremos que se aplique.

Una vez hecho esto ya podemos compilar el código cpp. Para ello, usamos la siguiente orden de nuestro compilador:

```bash
$ g++ basic.cpp -I /usr/include/python3.7 -I /usr/include/boost 
-lboost_python3 -shared -fPIC -o basic.so
```

Ahora veamos cómo usamos estas funciones en un script de Python. En primer lugar tenemos que importar el módulo que definíamos anteriormente como *basic*:

```python
import basic
```

Ahora ya podríamos recurrir a la función previamente implementada. Para probar su funcionamiento, usaremos distintos tipos de datos (*int*, *float* y *string*):

```python
print('\nGeneric functions')
print(basic.generic_sum(2, 2))
print(basic.generic_sum(19.1, 1.1))
print(basic.generic_sum("aaa", "bbb"))
```

Como vemos, llamamos a la función deseada recurriendo al módulo *basic* importado: ```basic.<funcion>(<argumentos>))```. Ejecutemos el script para comprobar los resultados obtenidos:

```bash
Generic functions
4.0
20.200000762939453
aaabbb
```

## Ejemplo de uso de objetos de Python en C++

> Si queremos ver un ejemplo más detallado de uso, podemos encontrarlo en *basicExamples/objetos.cpp* y *basicExamples/objetos.py*.

También podemos trabajar con objetos típicos de Python en el código de C++. Por ejemplo, podemos definir una lista de Python de la siguiente manera:

```cpp
bp::list lista;
```
Siendo ```bp``` el espacio de nombres de *Boost.Python* que hemos debido de declarar previamente.

Sobre esta lista podemos actuar tal y como lo haríamos en Python, como por ejemplo añadir elementos, eliminar elementos, etc. Si quisiéramos añadir un elemento a la lista, haríamos lo siguiente:

```cpp
lista.append(<elemento>);
```

Podemos usar también funciones estándar del lenguaje como *len()* por ejemplo de la siguiente manera:

```cpp
bp::ssize_t numKeys = bp::len(keyList);
```

Si, por ejemplo, queremos obtener las claves de un diccionario de Python, podemos hacerlo de la siguiente forma:

```cpp
bp::list keyList = dict.keys();
```

Hasta ahora, lo que hemos hecho ha sido emplear tipos de datos típicos de Python en el código de C++. Pero, por otro lado, si lo que queremos hacer es "*transformar*" un tipo de dato de Python a uno de C++, tenemos que recurrir a la función ```extract```. Con esta, lo que hacemos es intentar extraer el tipo de dato de Python a un tipo de dato de C++ que le especifiquemos: si es posible, lo realiza con éxito, si no lo fuera, se produciría un fallo. La sintáxis empleada es la siguiente:

```cpp
std::string key = bp::extract<std::string>(keyList[i]);
```

Como vemos, declaramos la variable (con un tipo de dato de C++) que portará el valor del objeto asociado en Python. Para hacer la extracción, indicamos el tipo de dato de C++ (```std::string```) y el objeto del que la realizamos. En este ejemplo, el objeto es una lista de claves de diccionario, concretamente la que hallábamos en el ejemplo anterior para ello. 

También podemos definir un objeto extractor en lugar de usar directamente el *extract* como anteriormente. La ventaja que tiene esto es que podemos comprobar previamente si la conversión a realizar por el extractor es correcta y se puede llevar a cabo. Un ejemplo de esto se puede ver en el siguiente fragmento de código:

```cpp
for (bp::ssize_t i = 0; i < length; i++){
    // Create extractor
    bp::extract<int> intExtractor(lista[i]);
    // Check if element can be extracted
    if (intExtractor.check()){
        // Add it to the list
        intList.append(intExtractor());
    }
}
```

Como vemos, vamos recorriendo todas las posiciones de una lista, y para cada una de ellas definimos su correspondiente extractor de enteros. Posteriormente, en el *if* comprobamos si dicha conversión a entero se puede realizar y, si es así, entonces añadimos ese valor a una lista auxiliar de enteros. De esta manera, lo que conseguimos es quedarnos únicamente con los valores enteros de la lista (puede haber varios tipos contenidos en una lista de Python).


## Ejemplo de uso de una clase de C++ en Python

> El código de este ejemplo podemos encontrarlo en el directorio *classExample*, contenido en los archivos *claseEjemplo.cpp* y *clase_ejemplo.py*.  

Para este ejemplo hemos implementado una clase sencilla de C++ y luego hemos sobrecargado uno de sus operadores, concretamente el de suma. La función de la clase es representar un punto 3D, por tanto, consta de tres coordenadas ($x$, $y$ y $z$). Debido a esto último tenemos que implementar una serie de funciones que nos permitan acceder y modificar dichos atributos privados (*setters* y *getters*). También se han incluido otras funciones: una para calcular la distancia entre dos puntos y otra para un objeto de la clase a string.

```cpp
template <typename T>
class Punto3D {
    private:
        T x, y, z;

    public:
        // Constructor
        Punto3D(T x, T y, T z): x(x), y(y), z(z) {}

        T getX() const
        {
            return this->x;
        }

        T getY() const
        {
            return this->y;
        }

        T getZ() const
        {
            return this->z;
        }

        void setX(T newX)
        {
            this->x = newX;
        }

        void setY(T newY)
        {
            this->y = newY;
        }

        void setZ(T newZ)
        {
            this->z = newZ;
        }

        double distancia(const Punto3D &p) const
        {
            return sqrt(pow(x - p.x, 2) + pow(y - p.y, 2) 
                        + pow(z - p.z, 2));
        }

        std::string toString() const
        {
            return "Punto3D -> x: " + std::to_string(this->x)
                                    + " y: " + std::to_string(this->y) 
                                    + " z: " + std::to_string(this->z);
        }
};
```

Como decíamos, además, hemos sobrecargado el operador de suma de la clase. El siguiente fragmento de código muestra como se ha llevado a cabo:

```cpp
template <typename T>
Punto3D<T> operator+(const Punto3D<T>& p1, const Punto3D<T>& p2)
{
    T newX = p1.getX() + p2.getX(),
      newY = p1.getY() + p2.getY(),
      newZ = p1.getZ() + p2.getZ();
    
    Punto3D<T> newP = Punto3D<T>(newX, newY, newZ);
    
    return newP;
}
```

Una vez tenemos el código de C++, hemos de pasar a crear el módulo de *Boost.Python*. En este caso tenemos que exponer la clase y, por tanto, sus correspondientes funciones y atributos:

```cpp
BOOST_PYTHON_MODULE(claseEjemplo){
    using namespace boost::python;

    class_<Punto3D<int>>("Punto3D", init<int, int, int>())
        .add_property("x", &Punto3D<int>::getX, &Punto3D<int>::setX)
        .add_property("y", &Punto3D<int>::getY, &Punto3D<int>::setY)
        .add_property("z", &Punto3D<int>::getZ, &Punto3D<int>::setZ)
        .def("distancia", &Punto3D<int>::distancia)
        .def("__str__", &Punto3D<int>::toString)
        .def(self + self);
}
```

Como vemos, lo que se ha hecho ha sido, en primer lugar, exponer la clase. Como estamos tratando con una clase genérica, tenemos que indicar el tipo de dato con el que queremos trabajar, también hemos de hacer esto a la hora de exponer el constructor: ```class_<NombreClase<T>>("Nombre Clase Python", init<T, T, T>())```. Justo después se procede a incluir sus atributos y sus respectivas funciones de modificación y consulta, para esto recurrimos a la función ```.add_property(<Nombre Attr Python>, <Getter>, <Setter>)```. Por otro lado, tenemos que añadir también las dos funciones implementadas pero esta vez con ```.def(<Nombre Python>, <Función>)```. El operador sobre cargado, tenemos que añadirlo también con ```.def``` pero indicando que intervienen dos objetos de la propia clase (```(self + self)```).

Veamos cómo el uso de esta clase en Python es realmente sencillo:

```python
# Importamos módulo
import claseEjemplo

# Declaración
p1 = claseEjemplo.Punto3D(1,1,1)
p2 = claseEjemplo.Punto3D(1,2,4)
p3 = p1

# Consulta
print(f"Punto 1 {p1}")
print(f"Punto 2 {p2}")
print(f"Punto 3 {p3}")

# Modificación
p3.y = 4

# Consulta
print(f"\nPunto 1 {p1}")
print(f"Punto 3 {p3}")

# Cálculo de distancia
dist = p1.distancia(p2)
print(f"\nDistancia entre los dos puntos: {dist}")

# Suma de dos objetos
print(f"\nSuma de los dos puntos: {p1 + p2}")
```

## Ejemplo más complejo: supresión de no máximos de una imagen

La supresión de no máximos de una imagen es un procedimiento costoso y de alto cómputo, es por esto por lo que seleccionamos este ejemplo para mostrar la diferencia entre usar un código completamente en Python y un código de Python que use módulos implementados con C++ puro. 

Las imágenes se encuentran representadas en un *array* de *numpy*. Por lo tanto, si queremos trabajar sobre ellas, será necesario recurrir también a dicha biblioteca dentro de C++. Por suerte, el propio *boost.python* nos permite esto mismo.
Para ello, debemos declararlo como un namespace de la siguiente manera: 

```cpp
namespace np = boost::python::numpy;
```

Ahora ya podemos trabajar con los *arrays* de dicha biblioteca tal y como lo haríamos en Python. Si, por ejemplo, quisiéramos crear un *numpy array* de ceros, haríamos lo siguiente:

```cpp
np::ndarray supr = np::zeros(shape, dtype);
```

Indicando que el tipo de dicho *array* corresponderá al tipo *ndarray* específico de dicha biblioteca. 

Lo explicado hasta el momento son algunos de los conceptos básicos que debemos conocer para trabajar con este tipo de dato. Ahora pasemos a usarlo en la supresión de no máximos de una imagen. 

La supresión de no máximos consiste en recorrer todos y cada uno de los píxeles de la imagen y comparar dicho pixel con su vecindario de 3x3: si el valor de dicho píxel es el máximo de su vecindario, entonces lo mantenemos, si no, lo eliminamos. 

### Comparativa

Comprobemos la diferencia de tiempos entre la ejecución de la supresión de no máximos en Python y este mismo proceso pero en Python usando Código de C++ puro mediante la biblioteca *Boost.Python*. 

El tiempo obtenido implementando el código con Python es el siguiente:

```bash
    Total time spent in non-max supression: 87.28784799575806
```

El tiempo empleado durante la ejecución del código que usa la biblioteca *Boost.Python* es el siguiente: 

```bash
    Total time spent in non-max supression: 53.51091933250427
```

Como vemos, hay una diferencia de tiempos notable. Es más, en el código de *Boost.Python*, por cada imagen se emplea alrededor de $0,55$ segundos:

```bash
[...]
Time in non-max supression: 0.6244661808013916
Time in non-max supression: 0.6220667362213135
Time in non-max supression: 0.5682306289672852
Time in non-max supression: 0.5632765293121338
Time in non-max supression: 0.5228853225708008
Time in non-max supression: 0.5326223373413086
[...]
```

En cambio, usando *Python* se tarda alrededor  de $0,9$ segundos:

```bash
[...]
Time in non-max supression: 0.9579119682312012
Time in non-max supression: 0.9638268947601318
Time in non-max supression: 0.970787763595581
Time in non-max supression: 0.8839678764343262
Time in non-max supression: 0.7947449684143066
Time in non-max supression: 0.812824010848999
[...]
```

# TODO explicar porque salen tantos tiempos

## Compilación: Makefile


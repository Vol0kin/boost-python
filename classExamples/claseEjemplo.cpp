# include <iostream>
# include <cmath>
# include <boost/python.hpp>

template <typename T>
class Punto3D {
    private:
        T x, y, z;

    public:
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
            return sqrt(pow(x - p.x, 2) + pow(y - p.y, 2) + pow(z - p.z, 2));
        }

        std::string toString() const
        {
            return "Punto3D -> x: " + std::to_string(this->x) + " y: " + std::to_string(this->y) + " z: " + std::to_string(this->z);
        }
};

template <typename T>
Punto3D<T> operator+(const Punto3D<T>& p1, const Punto3D<T>& p2)
{
    T newX = p1.getX() + p2.getX(),
      newY = p1.getY() + p2.getY(),
      newZ = p1.getZ() + p2.getZ();
    
    Punto3D<T> newP = Punto3D<T>(newX, newY, newZ);
    
    return newP;
}

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
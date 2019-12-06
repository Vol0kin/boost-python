#include <boost/python.hpp>
#include <string>
#include <cmath>

template <typename T>
T genericSum(T a, T b)
{
    return a + b;
}

int sumInts(int a, int b)
{
    return a + b;
}

float sumFloats(float a, float b)
{
    return a + b;
}

double sqrtNum(double num)
{
    return sqrt(num);
}

BOOST_PYTHON_MODULE(basic)
{
    using namespace boost::python;

    // Expose basic functions
    def("sum_ints", sumInts);
    def("sum_floats", sumFloats);
    def("sqrt_num", sqrtNum);

    // Expose generic function
    def("generic_sum", genericSum<int>);
    def("generic_sum", genericSum<float>);
    def("generic_sum", genericSum<std::string>);
}
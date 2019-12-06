#include <boost/python.hpp>
#include <string>

std::string helloWorld()
{
   return "Hello, world!";
}

BOOST_PYTHON_MODULE(hello)
{
    using namespace boost::python;

    // Expose 'helloWorld' function as 'greet'
    def("greet", helloWorld);
}
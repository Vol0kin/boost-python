#include <string>
#include <boost/python.hpp>
#include <iostream>

namespace bp = boost::python;

void checkListTypes(const bp::list& l)
{
    bp::ssize_t length = bp::len(l);

    // Iterate over the list
    for (bp::ssize_t i = 0; i < length; i++)
    {
        // Extract the object in the current position
        bp::object obj = bp::extract<bp::object>(l[i]);

        // Get the name of the class
        std::string objClassName = bp::extract<std::string>(
            obj.attr("__class__").attr("__name__")
        );

        std::cout << "Clase del objeto: " << objClassName << std::endl;
    }
}

bp::list getIntList(const bp::list& l)
{
    // Create new list
    bp::list intList;

    bp::ssize_t length = bp::len(l);

    for (bp::ssize_t i = 0; i < length; i++)
    {
        // Create extractor
        bp::extract<int> intExtractor(l[i]);

        // Check if element can be extracted
        if (intExtractor.check())
        {
            // Add it to the list
            intList.append(intExtractor());
        }
    }

    return intList;
}

void iterateDictionary(const bp::dict& dict)
{
    // Get keys
    bp::list keyList = dict.keys();

    bp::ssize_t numKeys = bp::len(keyList);

    for (bp::ssize_t i = 0; i < numKeys; i++)
    {
        std::string key = bp::extract<std::string>(keyList[i]);
        std::string val = bp::extract<std::string>(dict[key]);

        std::cout << key << ": " << val << std::endl;
    }
}

bp::list flatten2DList(const bp::list& l)
{
    bp::ssize_t length = bp::len(l);
    bp::list flattenedList;

    for (bp::ssize_t i = 0; i < length; i++)
    {
        bp::list innerList = bp::extract<bp::list>(l[i]);
        bp::ssize_t innerLength = bp::len(innerList);

        for (bp::ssize_t j = 0; j < innerLength; j++)
        {
            bp::object obj = bp::extract<bp::object>(innerList[j]);
            flattenedList.append(obj);
        }
    }

    return flattenedList;
}

BOOST_PYTHON_MODULE(objetos)
{
    using namespace bp;

    def("check_types", checkListTypes);
    def("get_int_list", getIntList);
    def("iterate_dict", iterateDictionary);
    def("flatten_2D_list", flatten2DList);
}
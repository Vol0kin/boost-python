#include <boost/python.hpp>
#include <boost/python/numpy.hpp>
#include <vector>

namespace bp = boost::python;
namespace np = boost::python::numpy;

np::ndarray nonMaxSupression(const bp::object& img)
{
    // Set up environment
    Py_Initialize();
    np::initialize();

    // Initialize shape and type
    bp::tuple shape = bp::extract<bp::tuple>(img.attr("shape"));
    np::dtype dtype = np::dtype::get_builtin<double>();
    
    // Create matrix
    np::ndarray supr = np::zeros(shape, dtype);

    int rows = bp::extract<int>(shape[0]),
        columns = bp::extract<int>(shape[1]);
    
    std::vector<double> region;

    for (int i = 0; i < rows; i++)
    {
        for (int j = 0; j < columns; j++)
        {
            double currentValue = bp::extract<double>(img[i][j]);
            region.clear();

            // Process 3x3 region
            for (int xReg = std::max(i-1, 0); xReg <= std::min(i+1, rows-1); xReg++)
            {
                for (int yReg = std::max(j-1, 0); yReg <= std::min(j+1, columns-1); yReg++)
                {
                    region.push_back(bp::extract<double>(img[xReg][yReg]));
                }
            }

            // Get max val from region
            auto max = std::max_element(region.begin(), region.end());

            // Copy current value if it's equal to the max value found
            if (*max == bp::extract<double>(img[i][j]))
            {
                supr[i][j] = img[i][j];
            }
        }        
    }

    return supr;
}

BOOST_PYTHON_MODULE(imageModule)
{
    def("non_max_supression", nonMaxSupression);
}

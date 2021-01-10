#!/usr/bin/python
import os

# Create the module path
module_path = 'autogen_module'
if not os.path.isdir(module_path):
    os.makedirs(module_path)
 
#dims = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','Eigen::Dynamic']
#dimTags = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','D']

dims =  ['1','2','3','4','5','6','Eigen::Dynamic']
dimTags = ['1','2','3','4','5','6','D']

#types =    ['char','short','int','long','unsigned char', 'unsigned short', 'unsigned int', 'unsigned long', 'float', 'double', 'std::complex<float>','std::complex<double>']
#typeTags = ['char','short','int','long','uchar', 'ushort', 'uint', 'ulong', 'float', 'double', 'cfloat','cdouble']
types = ['int', 'float', 'double', 'boost::uint8_t', 'boost::int64_t']
typeTags = ['int', 'float', 'double', 'uchar', 'long']



# Write a file for each type. This takes a long time to compile but
# it avoids using piles of memory during the compilation process.
with open('autogen_files.cmake','w') as cmakef:
    cmakef.write('SET(AUTOGEN_FILES\n\tsrc/autogen_module/numpy_eigen_export_module.cpp')
    for d1x in range(0,len(dims)):
        for d2x in range(0,len(dims)):
            for Tx in range(0,len(types)):
                cmakef.write('\n\tsrc/autogen_module/import_%s_%s_%s.cpp' % (dimTags[d1x], dimTags[d2x], typeTags[Tx]))
                with open(os.path.join('autogen_module/import_%s_%s_%s.cpp' % (dimTags[d1x], dimTags[d2x], typeTags[Tx])), 'w') as f:
                    f.write('// This file automatically generated by create_export_module.py\n')
                    f.write('#define NO_IMPORT_ARRAY \n\n')
                    f.write('#include <NumpyEigenConverter.hpp>\n\n')
                    f.write('#include <boost/cstdint.hpp>\n\n')
                    f.write('\n')
                    f.write('void import_%s_%s_%s()\n' % (dimTags[d1x], dimTags[d2x], typeTags[Tx]));
                    f.write('{\n')
                    f.write('\tNumpyEigenConverter<Eigen::Matrix< %s, %s, %s > >::register_converter();\n' % (types[Tx],dims[d1x],dims[d2x]))
                    f.write('}\n');
                    f.write('\n')
    cmakef.write('\n)\n')


# Now write out the top-level python export module that calls a function from each file above
with open(os.path.join(module_path,'numpy_eigen_export_module.cpp'),'w') as f:
    f.write('// This file automatically generated by create_export_module.py\n')
    f.write('#include <NumpyEigenConverter.hpp>\n\n')
    f.write('\n')
    f.write('// function prototypes\n')
    for d1 in dimTags:
        for d2 in dimTags:
            for T in typeTags:
                f.write('void import_%s_%s_%s();\n' % (d1, d2, T));
    f.write('\n')

    f.write('BOOST_PYTHON_MODULE(libnumpy_eigen)\n')
    f.write('{\n')
    f.write('\tusing namespace boost::python;\n')
    f.write('\t// Without this import, the converter will segfault\n');
    f.write('\timport_array();\n');
    f.write('\n');
    for d1 in dimTags:
        for d2 in dimTags:
            for T in typeTags:
                f.write('\timport_%s_%s_%s();\n' % (d1, d2, T));
    f.write('\n')
    f.write('}\n')
    f.write('\n')



###################################
## Now build the test module

# Create the module path
module_path = 'autogen_test_module'
if not os.path.isdir(module_path):
    os.makedirs(module_path)


with open('autogen_test_files.cmake','w') as cmakef:
    cmakef.write('SET(AUTOGEN_TEST_FILES\n\tsrc/autogen_test_module/numpy_eigen_test_module.cpp')
    for d1x in range(0,len(dims)):
        for d2x in range(0,len(dims)):
            for Tx in range(0,len(types)):
                cmakef.write('\n\tsrc/autogen_test_module/test_%s_%s_%s.cpp' % (dimTags[d1x], dimTags[d2x], typeTags[Tx]))
                with open(os.path.join('autogen_test_module/test_%s_%s_%s.cpp' % (dimTags[d1x], dimTags[d2x], typeTags[Tx])), 'w') as f:
                    td1 = d1x
                    td2 = d2x
                    f.write('#include <Eigen/Core>\n\n')
                    f.write('#include <numpy_eigen/boost_python_headers.hpp>\n')
                    f.write('Eigen::Matrix<%s, %s, %s> test_%s_%s_%s(const Eigen::Matrix<%s, %s, %s> & M)\n' % (types[Tx],dims[d1x],dims[d2x],typeTags[Tx],dimTags[td1],dimTags[td2],types[Tx],dims[d1x],dims[d2x]))
                    f.write('{\n')
                    f.write('\treturn M;\n')
                    f.write('}')
                    f.write('\n')
                    f.write('void export_%s_%s_%s()\n' % (typeTags[Tx],dimTags[td1],dimTags[td2]) )
                    f.write('{\n')
                    f.write('\tboost::python::def("test_%s_%s_%s",test_%s_%s_%s);\n' % (typeTags[Tx],dimTags[td1],dimTags[td2],typeTags[Tx],dimTags[td1],dimTags[td2]))
                    f.write('}\n\n')
    cmakef.write('\n)\n')



with open(os.path.join(module_path,'numpy_eigen_test_module.cpp'),'w') as f:
    f.write('// This file automatically generated by create_export_module.py\n')
    f.write('#include <numpy_eigen/boost_python_headers.hpp>\n')
    f.write('#include <Eigen/Core>\n\n')
    f.write('\n')
    f.write('// function prototypes\n')
    for d1x in range(0,len(dimTags)):
        for d2x in range(0,len(dimTags)):
            for Tx in range(0,len(typeTags)):
                td1 = d1x
                td2 = d2x

                f.write('void export_%s_%s_%s();\n' % (typeTags[Tx],dimTags[td1],dimTags[td2]))

    f.write('\n')
    f.write('BOOST_PYTHON_MODULE(libnumpy_eigen_test)\n')
    f.write('{\n')
    f.write('\n');
    for d1x in range(0,len(dimTags)):
        for d2x in range(0,len(dimTags)):
            for Tx in range(0,len(typeTags)):
                td1 = d1x
                td2 = d2x
                f.write('export_%s_%s_%s();\n' % (typeTags[Tx],dimTags[td1],dimTags[td2]))

    f.write('\n')
    f.write('}\n')
    f.write('\n')



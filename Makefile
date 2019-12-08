all: hello basic objetos class nonmax

.PHONY = all clean env

CXX = g++
FLAGS = -shared -fPIC
INCLUDE = -I /usr/include/python3.7 -I /usr/include/boost
BOOST = -lboost_python3
NUMPY = $(BOOST) -lboost_numpy3
OPT = -Os

hello: helloWorld/hello.cpp
	$(CXX) $< $(INCLUDE) $(BOOST) $(FLAGS) -o helloWorld/hello.so

basic: basicExamples/basic.cpp
	$(CXX) $< $(INCLUDE) $(BOOST) $(FLAGS) -o basicExamples/basic.so

objetos: basicExamples/objetos.cpp
	$(CXX) $< $(INCLUDE) $(BOOST) $(FLAGS) -o basicExamples/objetos.so

class: classExamples/claseEjemplo.cpp
	$(CXX) $< $(INCLUDE) $(BOOST) $(FLAGS) -o classExamples/claseEjemplo.so

nonmax: nonMaxSupression/imageModule.cpp
	$(CXX) $< $(INCLUDE) $(NUMPY) $(FLAGS) $(OPT) -o nonMaxSupression/imageModule.so

clean:
	rm -f ./*/*.so
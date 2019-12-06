all: hello basic

.PHONY = all clean

CXX = g++
FLAGS = -shared -fPIC
INCLUDE = -I /usr/include/python3.7 -I /usr/include/boost
BOOST = -lboost_python3

hello: helloWorld/hello.cpp
	$(CXX) $< $(INCLUDE) $(BOOST) $(FLAGS) -o helloWorld/hello.so

basic: basicExamples/basic.cpp
	$(CXX) $< $(INCLUDE) $(BOOST) $(FLAGS) -o basicExamples/basic.so

clean:
	rm -f ./*/*.so
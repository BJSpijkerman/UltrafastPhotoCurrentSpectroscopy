cmake_minimum_required(VERSION 3.14)
project(TwoTemperatureModel CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include_directories(include external)

find_package(yaml-cpp REQUIRED)

add_executable(ttm_sim main.cpp
	src/FileReader.cpp
	src/SplineHelpers.cpp
	src/AbsorptionModel.cpp
	src/YAMLParser.cpp
	src/Numerics.cpp
)

target_link_libraries(ttm_sim PRIVATE yaml-cpp::yaml-cpp)

set(OpenCV_DIR "E:/Tools/OpenCV-MinGW-Build-OpenCV-4.5.2-x64")

cmake_minimum_required(VERSION 3.0)

get_filename_component(ProjectId ${CMAKE_CURRENT_LIST_DIR} NAME)
string(REPLACE " " "_" ProjectId ${ProjectId})
project(${ProjectId} C CXX)
set (CMAKE_CXX_STANDARD 17)
find_package( OpenCV REQUIRED )

file(GLOB SOURCES  *.cpp)

add_executable(main ${SOURCES})
target_link_libraries(main ${OpenCV_LIBS})
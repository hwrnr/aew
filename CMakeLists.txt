cmake_minimum_required(VERSION 3.4.0)
cmake_policy(VERSION 3.0.2)

project(AEW LANGUAGES C VERSION 0.0.1 DESCRIPTION "AUR helper for (almost) every major distro")

if(NOT CMAKE_BUILD_TYPE)
	set(CMAKE_BUILD_TYPE Release)
endif()

set(CMAKE_VERBOSE_MAKEFILE OFF)
set(CMAKE_C_FLAGS "-Wall -Wextra")
set(CMAKE_C_FLAGS_DEBUG "-g")
set(CMAKE_C_FLAGS_RELEASE "-O3")

option(BUILD_SHARED_LIBS SHARED)

file(GLOB AEW_SOURCE_FILES src/*.c)
file(GLOB AEW_HEADER_FILES src/*.h)

find_package(CURL REQUIRED)
include_directories(${CURL_INCLUDE_DIR})

add_executable(aew ${AEW_SOURCE_FILES} ${AEW_HEADER_FILES})

target_link_libraries(aew ${CURL_LIBRARIES})

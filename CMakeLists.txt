cmake_minimum_required(VERSION 3.17)
project(competetions)

set(CMAKE_CXX_STANDARD 14)

add_executable(sol sol.cpp libs/ atcoder/ ./)

target_include_directories(sol PUBLIC
        "${PROJECT_SOURCE_DIR}"
        )

add_executable(hash hashcode_main.cpp libs/ python/t/pickles_txt python/y/pickles_txt python/p/pickles_txt hash_code_header.h)
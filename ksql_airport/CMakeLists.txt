cmake_minimum_required(VERSION 3.5)
project(ksql_airport)

if(NOT CMAKE_CXX_STANDARD)
 set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
 add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)

install(DIRECTORY launch media worlds
 DESTINATION share/${PROJECT_NAME}
)

ament_environment_hooks(env-hooks/99_ksql_airport_setup.sh.in)
ament_package()

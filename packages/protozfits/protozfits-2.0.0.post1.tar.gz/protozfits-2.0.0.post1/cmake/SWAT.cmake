adh_add_library(
    NAME swat
    SOURCES
        ${CMAKE_CURRENT_LIST_DIR}/../swat/swat_api.cpp
        ${CMAKE_CURRENT_LIST_DIR}/../swat/swat_data.cpp
        ${CMAKE_CURRENT_LIST_DIR}/../swat/swat_merge.cpp
        ${CMAKE_CURRENT_LIST_DIR}/../swat/swat_argv.cpp
        ${CMAKE_CURRENT_LIST_DIR}/../swat/swat_detector.cpp
        ${CMAKE_CURRENT_LIST_DIR}/../swat/swat_packet.cpp
        ${CMAKE_CURRENT_LIST_DIR}/../swat/swat_atlog.cpp
        ${CMAKE_CURRENT_LIST_DIR}/../swat/swat_dispatcher.cpp
        ${CMAKE_CURRENT_LIST_DIR}/../swat/swat_server.cpp
        ${CMAKE_CURRENT_LIST_DIR}/../swat/swat_builtin_client.cpp
        ${CMAKE_CURRENT_LIST_DIR}/../swat/swat_io.cpp
        ${CMAKE_CURRENT_LIST_DIR}/../swat/swat_signals.cpp
        ${CMAKE_CURRENT_LIST_DIR}/../swat/swat_config.cpp
        ${CMAKE_CURRENT_LIST_DIR}/../swat/swat_logger.cpp
        ${CMAKE_CURRENT_LIST_DIR}/../swat/swat_status.cpp
        ${CMAKE_CURRENT_LIST_DIR}/../swat/swat_control.cpp
        ${CMAKE_CURRENT_LIST_DIR}/../swat/swat_logger_nonacs.cpp
        ${CMAKE_CURRENT_LIST_DIR}/../swat/swat_support.cpp
        ${CMAKE_CURRENT_LIST_DIR}/../swat/swat_api_config.cpp
    PUBLIC_HEADERS
        ${CMAKE_CURRENT_LIST_DIR}/../swat/swat_api.h
        ${CMAKE_CURRENT_LIST_DIR}/../swat/swat_api_config.h
)

target_include_directories(swat PUBLIC ${CMAKE_CURRENT_LIST_DIR}/../swat)
target_compile_options(swat PRIVATE -std=c++11 -g -O1 -fPIC -Wno-write-strings -Wno-sign-compare)

target_link_libraries(swat PUBLIC Threads::Threads m)
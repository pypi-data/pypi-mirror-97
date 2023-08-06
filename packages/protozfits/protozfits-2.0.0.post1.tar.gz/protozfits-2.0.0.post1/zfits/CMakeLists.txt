
adh_add_library(
    NAME ZFitsIO
    SOURCES
        Checksum.cpp
        IZStream.cpp
        ricecomp.cpp
        MemoryManager.cpp
        ProtobufIFits.cpp
        ZIFits.cpp
        Huffman.cpp
        minilzo.cpp
        ProtobufToFits.cpp
        ProtobufZOFits.cpp
        ProtobufOFits.cpp
        ProtoSerialZOFits.cpp
        ZOFits.cpp
        IFits.cpp
        OFits.cpp
        FlatProtobufZOFits.cpp
    PUBLIC_HEADERS
        Checksum.h
        FitsDefs.h
        Huffman.h
        IFits.h
        IZStream.h
        lzoconf.h
        lzodefs.h
        MemoryManager.h
        minilzo.h
        OFits.h
        ProtobufIFits.h
        ProtobufToFits.h
        ProtobufZOFits.h
        ProtobufOFits.h
        ProtoSerialZOFits.h
        ricecomp.h
        ZIFits.h
        ZOFits.h
        Queue.h
        FlatProtobufZOFits.h
    LINK_LIBRARIES
        ADHCore
        zstd
        z
)

target_link_libraries(ZFitsIO PUBLIC ADHCore)
target_include_directories(ZFitsIO PUBLIC .)
target_compile_features(ZFitsIO PUBLIC cxx_std_11)
set_target_properties(
    ZFitsIO PROPERTIES
    CXX_EXTENSIONS OFF
    CXX_STANDARD_REQUIRED ON
)


add_executable(UnitTestAnyArrayTypesToFits UnitTestAnyArrayTypesToFits.cpp)
add_executable(UnitTestMultipleFitsTables UnitTestMultipleFitsTables.cpp)
add_executable(UnitTestProtobufZFits UnitTestProtobufZFits.cpp)
add_executable(UnitTestSimultaneousReadWrite UnitTestSimultaneousReadWrite.cpp)

target_link_libraries(UnitTestAnyArrayTypesToFits ZFitsIO zstd)
target_link_libraries(UnitTestMultipleFitsTables ZFitsIO zstd)
target_link_libraries(UnitTestProtobufZFits ZFitsIO zstd)
target_link_libraries(UnitTestSimultaneousReadWrite ZFitsIO zstd)

add_test(AnyArraysToFits UnitTestAnyArrayTypesToFits)
add_test(MultipleFitsTables UnitTestMultipleFitsTables)
add_test(SimultaneousReadWrite UnitTestSimultaneousReadWrite)
add_test(ZFitsCompression UnitTestProtobufZFits)

# TODO: need to add option(PYTHON "Build the python bindings to the zfits reader" ON) to top-level CMakeLists.txt
if(PYTHON)
    add_subdirectory(python)
endif()

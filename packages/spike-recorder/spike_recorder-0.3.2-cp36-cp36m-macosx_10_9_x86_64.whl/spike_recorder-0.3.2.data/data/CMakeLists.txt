cmake_minimum_required(VERSION 3.15...3.18)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# SET(CMAKE_BUILD_TYPE Debug)

project(spike_recorder VERSION "0.0.1")

if(UNIX AND NOT APPLE)
	set(LINUX TRUE)
endif()

# Currently, Scikit-build does not support FindPython, so we convert the
# provided hints ourselves.
if(SKBUILD)
  set(Python_EXECUTABLE "${PYTHON_EXECUTABLE}")
  set(Python_INCLUDE_DIR "${PYTHON_INCLUDE_DIR}")
  set(Python_LIBRARY "${PYTHON_LIBRARY}")
  set(DUMMY "${PYTHON_VERSION_STRING}")  # Not needed, silences a warning
endif()

set(Python_FIND_IMPLEMENTATIONS CPython PyPy)  # PyPy requires 3.18
find_package(Python REQUIRED COMPONENTS Interpreter Development)

# Scikit-Build does not add your site-packages to the search path automatically,
# so we need to add it _or_ the pybind11 specific directory here.
execute_process(
  COMMAND
    "${Python_EXECUTABLE}" -c
    "import pybind11; print(pybind11.get_cmake_dir())"
  OUTPUT_VARIABLE _tmp_dir
  OUTPUT_STRIP_TRAILING_WHITESPACE COMMAND_ECHO STDOUT)
list(APPEND CMAKE_PREFIX_PATH "${_tmp_dir}")

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/extern/Spike-Recorder/cmake")

# Now we can find pybind11
find_package(pybind11 CONFIG REQUIRED)

find_package(hidapi)
find_package(SDL2 REQUIRED)
find_package(sdl2-image CONFIG REQUIRED)
find_package(OpenGL REQUIRED COMPONENTS OpenGL)
find_package(cppzmq REQUIRED)
find_package(BASS REQUIRED)
find_package(nlohmann_json REQUIRED)


# If macos or linux, SDL2 sets -Wl,-undefined,error, we need to overide this
# for pybind11 linking because it seems to expect to use dynamic lookup to find
# the Python libraries. All of this seems like a big hack, FIXME
if (LINUX OR APPLE)
  get_target_property(SDL_LIBS SDL2::SDL2-static IMPORTED_LINK_INTERFACE_LIBRARIES_RELEASE)
  string(REPLACE "-Wl,-undefined,error;" "" SDL_LIBS_FIX "${SDL_LIBS}")
  string(REPLACE "-Wl,--no-undefined;" "" SDL_LIBS_FIX "${SDL_LIBS_FIX}")
  set_property(TARGET SDL2::SDL2-static PROPERTY IMPORTED_LINK_INTERFACE_LIBRARIES_RELEASE "${SDL_LIBS_FIX}")  
  #set_property(TARGET SDL2::SDL2-static APPEND PROPERTY IMPORTED_LINK_INTERFACE_LIBRARIES_RELEASE "-Xlinker -undefined;-Xlinker dynamic_lookup")
endif()


# General include directories for the Spike-Recorder application
include_directories("extern/Spike-Recorder/src" "extern/Spike-Recorder/src/libraries" "extern/Spike-Recorder/support")

file(GLOB SOURCES
        "extern/Spike-Recorder/src/*.cpp"
        "extern/Spike-Recorder/src/widgets/*.cpp"
        "extern/Spike-Recorder/src/engine/*.cpp"
        "extern/Spike-Recorder/src/libraries/*.cpp")

# Need to remove some firmware upgrade source, this is disabled for all builds for now
list(FILTER SOURCES EXCLUDE REGEX "FirmwareUpdateView.cpp")

# Also remove main, we are building a shared library\pybind11 module
list(FILTER SOURCES EXCLUDE REGEX "main.cpp")

# Add OS specific source files and libs
if (WIN32)
	list(APPEND SOURCES
			"extern/Spike-Recorder/src/native/PathsWin.cpp"
			"extern/Spike-Recorder/src/widgets/native/FileDialogWin.cpp"
			"extern/Spike-Recorder/src/defaults/DefaultConfig.cpp")

	# setupapi.lib is needed for some functions in HID code on windows it seems. MSVC knows where this lib is so just need
	# to add it by name.
	list(APPEND PLATFORM_LIBS "setupapi.lib")
elseif (LINUX)
	list(APPEND SOURCES
			"extern/Spike-Recorder/src/native/PathsLinux.cpp"
			"extern/Spike-Recorder/src/widgets/native/FileDialogLinux.cpp")
elseif (APPLE)
	list(APPEND SOURCES
		"extern/Spike-Recorder/src/native/PathsMac.cpp"
		"extern/Spike-Recorder/src/native/KeyboardGeneratorMac.cpp"
		"extern/Spike-Recorder/src/native/SerialPortsScanMac.cpp"
		"extern/Spike-Recorder/src/widgets/native/FileDialogMac.cpp"
		"extern/Spike-Recorder/src/widgets/native/FileDialogMac.mm"
		"extern/Spike-Recorder/src/defaults/DefaultConfig.cpp"
		)
endif ()

pybind11_add_module(_core MODULE src/spike_recorder_mod.cpp ${SOURCES})

target_link_libraries(_core PUBLIC
	SDL2::SDL2-static
	SDL2::SDL2_image
	hidapi::hidapi
	OpenGL::GL
	BASS
	cppzmq
	nlohmann_json::nlohmann_json
	${PLATFORM_LIBS})

target_compile_definitions(_core PUBLIC -DSIGSLOT_PURE_ISO -DSDL_MAIN_HANDLED)

if (WIN32)
	target_compile_definitions(_core PUBLIC -D_USE_MATH_DEFINES -DNOMINMAX)
	set_property(TARGET _core PROPERTY MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>")
endif ()

# We need to copy data/ to the build directory too
add_custom_command(TARGET _core POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_directory
    ${CMAKE_CURRENT_LIST_DIR}/extern/Spike-Recorder/data
    $<TARGET_FILE_DIR:_core>/data
)
install(DIRECTORY $<TARGET_FILE_DIR:_core>/data DESTINATION .)

# Add a post build command to copy bass runtime libs
if (WIN32)
  add_custom_command(TARGET _core POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_if_different
    "${CMAKE_CURRENT_BINARY_DIR}/bass/x64/bass.dll"
    "${CMAKE_CURRENT_BINARY_DIR}/bass/x64/bass_aac.dll"
    "${CMAKE_CURRENT_BINARY_DIR}/bass/x64/bassalac.dll"
    $<TARGET_FILE_DIR:_core>)

    install(FILES $<TARGET_FILE_DIR:_core>/bass.dll DESTINATION .)
    install(FILES $<TARGET_FILE_DIR:_core>/bass_aac.dll DESTINATION .)
    install(FILES $<TARGET_FILE_DIR:_core>/bassalac.dll DESTINATION .)

endif()
if (LINUX)
  add_custom_command(TARGET _core POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_if_different
    "${CMAKE_CURRENT_BINARY_DIR}/bass/x64/libbass.so"
    "${CMAKE_CURRENT_BINARY_DIR}/bass/x64/libbass_aac.so"
    "${CMAKE_CURRENT_BINARY_DIR}/bass/x64/libbassalac.so"
    $<TARGET_FILE_DIR:_core>)

    install(FILES $<TARGET_FILE_DIR:_core>/libbass.so DESTINATION .)
    install(FILES $<TARGET_FILE_DIR:_core>/libbass_aac.so DESTINATION .)
    install(FILES $<TARGET_FILE_DIR:_core>/libbassalac.so DESTINATION .)

endif()
if (APPLE)
  add_custom_command(TARGET _core POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_if_different
    "${CMAKE_CURRENT_BINARY_DIR}/bass/libbass.dylib"
    $<TARGET_FILE_DIR:_core>)

    install(FILES $<TARGET_FILE_DIR:_core>/libbass.dylib DESTINATION .)
endif()

target_compile_definitions(_core PRIVATE VERSION_INFO=${PROJECT_VERSION})

install(TARGETS _core DESTINATION .)

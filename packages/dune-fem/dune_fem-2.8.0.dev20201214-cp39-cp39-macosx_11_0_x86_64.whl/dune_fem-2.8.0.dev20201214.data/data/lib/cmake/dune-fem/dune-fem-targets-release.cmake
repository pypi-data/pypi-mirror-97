#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "dunefem" for configuration "Release"
set_property(TARGET dunefem APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(dunefem PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libdunefem.a"
  )

list(APPEND _IMPORT_CHECK_TARGETS dunefem )
list(APPEND _IMPORT_CHECK_FILES_FOR_dunefem "${_IMPORT_PREFIX}/lib/libdunefem.a" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)

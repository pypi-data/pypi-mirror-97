#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "dumux_fmt" for configuration "Release"
set_property(TARGET dumux_fmt APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(dumux_fmt PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libdumux_fmt.a"
  )

list(APPEND _IMPORT_CHECK_TARGETS dumux_fmt )
list(APPEND _IMPORT_CHECK_FILES_FOR_dumux_fmt "${_IMPORT_PREFIX}/lib/libdumux_fmt.a" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)

#----------------------------------------------------------------
# Generated CMake target import file for configuration "Debug".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "t3_action_msg::t3_action_msg__rosidl_typesupport_fastrtps_c" for configuration "Debug"
set_property(TARGET t3_action_msg::t3_action_msg__rosidl_typesupport_fastrtps_c APPEND PROPERTY IMPORTED_CONFIGURATIONS DEBUG)
set_target_properties(t3_action_msg::t3_action_msg__rosidl_typesupport_fastrtps_c PROPERTIES
  IMPORTED_LOCATION_DEBUG "${_IMPORT_PREFIX}/lib/libt3_action_msg__rosidl_typesupport_fastrtps_c.so"
  IMPORTED_SONAME_DEBUG "libt3_action_msg__rosidl_typesupport_fastrtps_c.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS t3_action_msg::t3_action_msg__rosidl_typesupport_fastrtps_c )
list(APPEND _IMPORT_CHECK_FILES_FOR_t3_action_msg::t3_action_msg__rosidl_typesupport_fastrtps_c "${_IMPORT_PREFIX}/lib/libt3_action_msg__rosidl_typesupport_fastrtps_c.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)

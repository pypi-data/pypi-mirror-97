set(PACKAGE_VERSION "2.8.0")

if("${PACKAGE_FIND_VERSION_MAJOR}" EQUAL "2" AND
     "${PACKAGE_FIND_VERSION_MINOR}" EQUAL "8")
  set (PACKAGE_VERSION_COMPATIBLE 1) # compatible with newer
  if ("${PACKAGE_FIND_VERSION}" VERSION_EQUAL "2.8.0")
    set(PACKAGE_VERSION_EXACT 1) #exact match for this version
  endif()
endif()

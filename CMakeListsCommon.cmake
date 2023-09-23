set(CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_STANDARD 17)

if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
    add_compile_options(
        -fPIC

        -pedantic
        -pedantic-errors

        -Wall
        -Wextra
        -Werror

        -Waligned-new
        -Walloca
        -Walloc-zero
        -Wcast-align
        -Wcast-qual
        -Wconditionally-supported
        -Wconversion
        -Wdisabled-optimization
        -Wdouble-promotion
        -Wduplicated-cond
        -Wfloat-conversion
        -Wformat
        -Wformat-security
        -Wformat-signedness
        -Wlogical-op
        -Wmissing-include-dirs
        -Wnoexcept
        -Wnon-virtual-dtor
        -Wnull-dereference
        -Wold-style-cast
        -Woverloaded-virtual
        -Wpacked
        -Wredundant-decls
        -Wshadow
        -Wsized-deallocation
        -Wstrict-aliasing
        -Wstrict-null-sentinel
        -Wtrampolines
        -Wundef
        -Wuninitialized
        -Wuseless-cast
        -Wvla
        -Wzero-as-null-pointer-constant

        -Wno-unused-function
    )
    set(PLATFORM_DIR Linux/x64/g++-${CMAKE_CXX_COMPILER_VERSION})

elseif(MSVC)
    add_compile_definitions(
        # Preventing definition of the 'min' & 'max' macros
        # See: https://stackoverflow.com/questions/5004858/why-is-stdmin-failing-when-windows-h-is-included
        NOMINMAX
        # Ignoring security warnings that have more secure non-standard (MSVC-specific) versions
        # See: https://learn.microsoft.com/en-us/cpp/c-runtime-library/security-features-in-the-crt#eliminating-deprecation-warnings
        # Some can be automatically used by defining _CRT_SECURE_CPP_OVERLOAD_STANDARD_NAMES, and yet others with
        #   _CRT_SECURE_CPP_OVERLOAD_STANDARD_NAMES_COUNT. However, as not all are available (notably std::getenv()),
        #   and as this might perhaps change the behavior, these definitions have not been used
        # See: https://learn.microsoft.com/en-us/cpp/c-runtime-library/secure-template-overloads
        _CRT_SECURE_NO_WARNINGS
    )

    add_compile_options(
        /permissive-
        /Zc:__cplusplus
        /Zc:externConstexpr
        /Zc:inline
        /Zc:preprocessor
        /Zc:throwingNew

        /W4
        /WX

        /utf-8
        /diagnostics:caret
    )

    if(CMAKE_CXX_COMPILER_VERSION VERSION_GREATER_EQUAL 19.34)
        add_compile_options(
            /Zc:enumTypes
        )
    endif()
    if(CMAKE_CXX_COMPILER_VERSION VERSION_GREATER_EQUAL 19.35)
        add_compile_options(
            /Zc:templateScope
        )
    endif()

    set(PLATFORM_DIR Windows/x64/vc${CMAKE_CXX_COMPILER_VERSION})

endif()

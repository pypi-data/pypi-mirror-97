# Makefile for repack
#
# `make` - Build and compile the pytips package.
# `make clean` - Remove all compiled (non-source) files that are created.
#
# If you are interested in the commands being run by this makefile, you may add
# "VERBOSE=1" to the end of any `make` command, i.e.:
#
#               make VERBOSE=1
#
# This will display the exact commands being used for building, etc.
#

LIBDIR = repack/utils/

# Set verbosity
#
Q = @
O = > /dev/null
ifdef VERBOSE
        ifeq ("$(origin VERBOSE)", "command line")
                Q =
                O =
        endif
endif

all:
	@echo "Building repack package."
	$(Q)python setup.py build $(O)
	@mv -f build/lib.*/$(LIBDIR)/*.so ./$(LIBDIR)
	@rm -rf build/
	@echo "Successful compilation."

clean:
	rm -rf $(LIBDIR)*.so

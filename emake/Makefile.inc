###########################################################
# Makefile.inc
###########################################################
# wildcard variables from Makefile
sources:=$(wildcard $(SOURCES))
target:=$(TARGET)

other_makefiles=$(wildcard $(OTHER_MAKEFILES))

###########################################################
# Environment Variables
#
EMAKE_HOME=$(shell emake --home)
MAKEFILE_FOR_LANGUAGE=$(EMAKE_HOME)/lang/Makefile-$(PROGRAMMING_LANGUAGE)


###########################################################
# Options to be used for all makefiles
#
MAKE=make


###########################################################
# Rules && Commands
#
all:premake all-$(PROGRAMMING_LANGUAGE) ;

premake:
	@for mk in $(other_makefiles); do \
		$(MAKE) -C $$(dirname $$(mk)) -f $$(basename $$(mk)) || exit -1; \
	done


include $(MAKEFILE_FOR_LANGUAGE)
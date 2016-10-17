#!/bin/bash
declare -A allopts=()
declare -A options=()
makefile_name=Makefile

allopts_init(){
	local oifs=$IFS IFS=";"
	local optstrs=(${option_table})
	IFS=$oifs

	for i in ${!optstrs[@]}
	do
		local optstr=$(echo ${optstrs[$i]})
		if [[ -z $optstr ]]; then
			continue
		fi
		# echo $optstr
		local name=${optstr%%:*}
		local value=${optstr#*:}
		# echo k=$name
		# echo v=$value

		for desc in $value
		do
			if [[ -n ${allopts[$desc]} ]]; then
				echo "[Error]Conflict found."; exit -1
			fi
			# echo v: $desc
			# echo e: ${allopts[$desc]}
			allopts[$desc]=$name
		done 
	done 
}


parse_params(){
	allopts_init 

	local name=
	local value=
	local hasval=

	while [ $# -gt 0 ]
	do
		if [[ $1 == --* ]]; then
			if [[ $1 == *=* ]]; then
				name=${1%%=*}
				value=${1#*=}
				hasv=true
			else
				name=$1
				value=true
				hasv=false
			fi
			
			optname=${allopts[$name]}
			if [[ -z $optname ]]; then
				echo "invalid option: $name"; exit -1
			fi
			if [[ $optname == *\? ]]; then
				if [[ hasv == false ]]; then
					echo "no value given for option $name"; exit -1
				fi 
			else
				if [[ hasv == true ]]; then
					echo "no value requried for option $name"; exit -1
				fi 
			fi
			${options[$optname]}=$value

		elif [[ $1 == -* ]]; then
			optname=${allopts[$1]}
			if [[ -z $optname ]]; then
				echo "invalid option: $1"; exit -1
			fi
			if [[ $optname == *\? ]]; then
				if [ $# -gt 1 ]; then
					shift && value=$1
				else
					echo "no value required for option $1"; exit -1
				fi
			else
				value=true
			fi
			options[$optname]=$value
		else
			makefile_name=$1
			break
		fi
		shift 
	done 
}

render(){
	line=$(echo ${1#\#!*})
	# echo $line
	if [[ -z $line ]]; then
		echo "" && return
	fi

	cmd=${line%% *}
	rest_text=${line#* }

	case $cmd in
		"set")
			render_for_set $rest_text
			;;
		"include")
			render_for_include $rest_text
			;;
		*)
			echo invalid cmd: $cmd ; exit -1
			;;
	esac
}

render_for_set(){
	echo $1=$(render_map $2)
}

render_for_include(){
	echo reserving...; exit -1
}

render_map(){
	# echo "xxxxxx:" $1
	case $1 in 
		"lang")
			echo ${options["lang?"]}
			;;
		"makefile_name")
			echo ${makefile_name}
			;;
		*)
			echo "invalid key:$1"
			;;
	esac
}

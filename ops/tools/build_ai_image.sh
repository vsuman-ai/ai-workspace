#!/bin/bash
MODULE_NAME="$1"
DEPS_PEX="$2"
SRCS_PEX="$3"
BASE_IMAGE="$4"
CACHE_IMAGE="$5"
shift
shift
shift
shift
shift

echo "MODULE_NAME: $MODULE_NAME"
echo "DEPS_PEX: $DEPS_PEX"
echo "SRCS_PEX: $SRCS_PEX"
echo "BASE_IMAGE: $BASE_IMAGE"
echo "CACHE_IMAGE: $CACHE_IMAGE"

function convert_to_file_path {
	echo $1 | sed -r s/\\//\./g | sed -r s/\:/\\//g
}

function print_line {
	echo "----------------------------------------"
}

DEPS_PEX_FILE="dist/"$(convert_to_file_path $DEPS_PEX)".pex"
SRCS_PEX_FILE="dist/"$(convert_to_file_path $SRCS_PEX)".pex"

function notify_fail {
	echo "Building image failed!"
	exit -1
}


print_line
echo -e "Building pex files for $MODULE_NAME srcs=$SRCS_PEX deps=$DEPS_PEX ..\n\n"
docker buildx build --progress=plain \
docker buildx build --progress=plain --load \
	--build-arg MODULE_NAME=$MODULE_NAME \
	--build-arg CACHE_IMAGE=${CACHE_IMAGE} \
	--build-arg BASE_IMAGE=${BASE_IMAGE} \
	--build-arg deps_pex=$DEPS_PEX_FILE \
	--build-arg srcs_pex=$SRCS_PEX_FILE \
	--build-arg deps_pex_target=$DEPS_PEX \
	--build-arg srcs_pex_target=$SRCS_PEX -f ops/pex.Dockerfile . "$@"
print_line


echo -e "Building cache image"
docker buildx build \
	--progress=plain \
	--progress=plain --load \
	-f ops/cache.Dockerfile -t ${CACHE_IMAGE} .
print_line

#!/bin/bash


# Note: this is an example file to showcase a common pipeline used to generate
# a viewable report of the dependencies of a target package

# Example usage:
# ./generate_dependencies_pdf.sh  /net/pipeline-ia/dev/vviperin/2020.1/commslib

package_root="$1"
if [ ! -d "$package_root" ]; then
    echo "$package_root could not be found on disk."
    echo "Please provide a correct path!"
    exit 1
fi

package_name=$(basename $package_root)
tmp_dir="/tmp/snake-food/deps/$package_name"

echo "Examining dependencies of $package_name"

pushd .

if [ -d "$tmp_dir" ]; then
    rm -rf "$tmp_dir"
fi

mkdir -p "$tmp_dir"
cd "$tmp_dir"

# Generate raw dependencies of the package
sfood "$package_root" > "${package_name}.deps"

# Generate the 'clusters' that you want to use for grouping them
ls -1d "$package_root" > "$package_name}_clusters"

# Aggregate the imports
cat "${package_name}.deps" | sfood-cluster -f "$package_name}_clusters" > "${package_name}_clusters.deps"

# Generate the final image
cat "${package_name}_clusters.deps" | sfood-graph -p | dot -Tpng -Gdpi=1000 -o "${package_name}_deps.png"

echo "PNG generated in $tmp_dir/${package_name}_deps.png"

popd

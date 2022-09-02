# Builds Development Containers
#
#
PIGNUS_DIR="/home/kube/pignus"
PIGNUS_SRC="/home/kube/pignus/src"
PIGNUS_TAG="0.0.1"

# Add Source
cp -r /home/kube/repos/pignus/src/ /home/kube/repos/pignus/docker/pignus-api/
rm -rf /home/kube/repos/pignus/docker/pignus-api/src/build
rm -rf /home/kube/repos/pignus/docker/pignus-api/src/dist
rm -rf /home/kube/repos/pignus/docker/pignus-api/src/pignus.egg-info

# Add Tests
cp -r /home/kube/repos/pignus/tests/ /home/kube/repos/pignus/docker/pignus-api/

# cp -r /home/kube/repos/pignus/test/ /home/kube/repos/pignus/docker/pignus-api
cd /home/kube/repos/pignus/docker/pignus-api
docker build -t politeauthority/pignus-api:${PIGNUS_TAG} .

# Remove the source
rm -rf /home/kube/repos/pignus/docker/pignus-api/src
rm -rf /home/kube/repos/pignus/docker/pignus-api/tests

echo "Build complete!"
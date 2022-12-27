# Builds Development Containers
#
#
PIGNUS_DIR="/Users/alix/Programming/repos/pignus/"
PIGNUS_TAG="0.0.1"

# Add Source
cp -r ${PIGNUS_DIR}/src ${PIGNUS_DIR}/docker/pignus-api/
rm -rf ${PIGNUS_DIR}/docker/pignus-api/src/build
rm -rf ${PIGNUS_DIR}/docker/pignus-api/src/dist
rm -rf ${PIGNUS_DIR}/docker/pignus-api/src/pignus.egg-info

# Add Tests
cp -r ${PIGNUS_DIR}/tests/ ${PIGNUS_DIR}/docker/pignus-api/

# cp -r /home/kube/repos/pignus/test/ /home/kube/repos/pignus/docker/pignus-api
cd ${PIGNUS_DIR}/docker/pignus-api
docker build -t politeauthority/pignus-api:${PIGNUS_TAG} .

# Remove the source
rm -rf ${PIGNUS_DIR}/docker/pignus-api/src
rm -rf ${PIGNUS_DIR}/docker/pignus-api/tests

echo "Build complete!"
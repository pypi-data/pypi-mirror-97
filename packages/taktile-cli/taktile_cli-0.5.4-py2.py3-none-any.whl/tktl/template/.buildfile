FROM taktile/base-serving-api-arrow:__version__ AS build_step

ENV APPDIR /app

WORKDIR $APPDIR

# Install requirements
COPY ./requirements.txt ${APPDIR}/user_requirements.txt
RUN pip install -r ${APPDIR}/user_requirements.txt

# Copy code and assets for running the application
COPY ./src ${APPDIR}/src
COPY ./assets ${APPDIR}/assets
COPY ./tests ${APPDIR}/user_tests

#
# DO NOT EDIT ANYTHING BELOW THIS COMMENT
#
FROM build_step

ARG RESOURCE_NAME
ARG DEPLOYMENT_API_URL
ARG COMMIT_HASH
ARG LOCAL_CLUSTER
ARG TAKTILE_UPDATE_KEY
ARG REMOTE_ARG=unset


WORKDIR /kaniko/buildcontext/

RUN git lfs install
RUN git config remote.origin.url $REMOTE_ARG
RUN git lfs pull origin
COPY ./assets ${APPDIR}/assets

WORKDIR $APPDIR

# Run tests conditionally
RUN bash /app/scripts/run-tests-and-export.sh $COMMIT_HASH $TAKTILE_UPDATE_KEY $DEPLOYMENT_API_URL $LOCAL_CLUSTER $RESOURCE_NAME

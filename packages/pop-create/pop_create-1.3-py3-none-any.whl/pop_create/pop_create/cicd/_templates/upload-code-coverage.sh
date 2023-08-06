set -ex
if [ ! -f codecov.sh ]; then
  n=0
  until [ "$n" -ge 5 ]
  do
  if curl --max-time 30 -L https://codecov.io/bash --output codecov.sh; then
      break
  fi
    n=$((n+1))
    sleep 15
  done
fi
export PY_VERSION=$(python -c "import sys; print('{}{}'.format(*sys.version_info))")
export REPORT_NAME="Py${PY_VERSION}-Project"
export REPORT_FLAGS="py${PY_VERSION},project"
export REPORT_PATH="artifacts/coverage-project.xml"
if [ -f codecov.sh ] && [ -f $REPORT_PATH ]; then
  n=0
  until [ "$n" -ge 5 ]
  do
    if bash codecov.sh -R $(pwd) -n "${REPORT_NAME}" -f "${REPORT_PATH}" -F "${REPORT_FLAGS}"; then
      break
    fi
    n=$((n+1))
    sleep 15
  done
fi
export REPORT_NAME="Py${PY_VERSION}-Tests"
export REPORT_FLAGS="py${PY_VERSION},tests"
export REPORT_PATH="artifacts/coverage-tests.xml"
if [ -f codecov.sh ] && [ -f $REPORT_PATH ]; then
  n=0
  until [ "$n" -ge 5 ]
  do
    if bash codecov.sh -R $(pwd) -n "${REPORT_NAME}" -f "${REPORT_PATH}" -F "${REPORT_FLAGS}"; then
      break
    fi
    n=$((n+1))
    sleep 15
  done
fi

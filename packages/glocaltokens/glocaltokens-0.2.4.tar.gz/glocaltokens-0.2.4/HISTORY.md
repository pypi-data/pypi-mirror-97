### v0.2.4
#### Changes

#### 🚀 Features

- Expose hardware name in the Device @leikoilja (#38)

#### 🐛 Bug Fixes

- Fix authentication (401) error in `get_homegraph` @ArnyminerZ (#37)

### v0.2.3
#### Changes

#### 🚀 Features

- Added zeroconf instance passing. @ArnyminerZ (#34)


### v0.2.2
#### Changes

- Removing redundant `uuid` dependency from package setup

### v0.2.1
#### Changes

- Zeroconf import @ArnyminerZ (#32)

#### 🚀 Features

- Adding client tests for fetching tokens @leikoilja (#30)
- Grpcio tools version @ArnyminerZ (#29)

#### 🧰 Maintenance

- Get devices testing @ArnyminerZ (#31)


### v0.2.0
#### Changes

- Adding support for python 3.9 @leikoilja (#26)
- Adding isort to pre-commit and github action @leikoilja (#25)
- Adding logging and pre-commit hooks @leikoilja (#19)
- Added access token expiration @ArnyminerZ (#9)
- Update explanation to make sure that others use your script corretly @DurgNomis-drol (#10)

#### 🚀 Features

- Added device IP discovery @ArnyminerZ (#13)
- Testing environment @leikoilja (#15)

#### 🔧 Enhancement

- Implement typing @ArnyminerZ (#22)
- Improve Android ID generation @leikoilja (#24)

#### 🧰 Maintenance

- Implement typing @ArnyminerZ (#22)


### v0.1.4
- Pinning `grpcio==1.31.0` dependency to match with HomeAssistant's version


### v0.1.3
- Removing `jq` dependency, thanks @DurgNomis-drol


### v0.1.2
- Removing dependency `requests==2.23.0` since `gpsoauth` is supporting newest versions


### v0.1.1
- Fixing the `GetHomeGraphResponse.Home.Device.State.value` serialization issue


### v0.1
- Initial release

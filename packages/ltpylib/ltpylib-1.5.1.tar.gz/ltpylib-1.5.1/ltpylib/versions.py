#!/usr/bin/env python
import semver


class LenientVersionInfo(semver.VersionInfo):

  def __init__(self, version: str):
    self.original_version: str = version

    self.version = version
    if self.version.count(".") <= 0:
      self.version = self.version + ".0.0"
    elif self.version.count(".") <= 1:
      self.version = self.version + ".0"

    parsed = semver.parse_version_info(self.version)
    semver.VersionInfo.__init__(self, parsed.major, parsed.minor, parsed.patch, parsed.prerelease, parsed.build)

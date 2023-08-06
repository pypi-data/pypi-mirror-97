#!/usr/bin/env python
import unittest

from ltpylib.mvnutil import MavenArtifact

has_all = MavenArtifact(
  group_id="com.lancethomps",
  artifact_id="lava",
  version="1.0.0",
  packaging="jar",
  classifier="shaded",
  scope="runtime",
)
has_group_artifact = MavenArtifact(**{k: getattr(has_all, k) for k in ["group_id", "artifact_id"]})
has_artifact = MavenArtifact(**{k: getattr(has_all, k) for k in ["artifact_id"]})
has_group_artifact_classifier = MavenArtifact(**{k: getattr(has_all, k) for k in ["group_id", "artifact_id", "classifier"]})
artifacts = [
  has_all,
  has_group_artifact,
  has_artifact,
  has_group_artifact_classifier,
]


class TestMavenArtifact(unittest.TestCase):

  def test_to_artifact_string(self):
    assert has_all.to_artifact_string() == "com.lancethomps:lava:1.0.0:jar:shaded:runtime"
    assert has_group_artifact.to_artifact_string() == "com.lancethomps:lava"
    assert has_artifact.to_artifact_string() == "*:lava"
    assert has_group_artifact_classifier.to_artifact_string() == "com.lancethomps:lava:*:*:shaded"

  def test_from_artifact_string(self):
    for artifact in artifacts:
      assert artifact == MavenArtifact.from_artifact_string(artifact.to_artifact_string(), strict=False)


if __name__ == '__main__':
  unittest.main()

# -*- coding: utf-8 -*- #
# Copyright 2024 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Factory class for RayBatch message."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.command_lib.dataproc import flags
from googlecloudsdk.command_lib.dataproc import local_file_uploader


class RayBatchFactory(object):
  """Factory class for RayBatch message."""

  def __init__(self, dataproc):
    """Factory class for RayBatch message.

    Args:
      dataproc: A Dataproc instance.
    """
    self.dataproc = dataproc

  def UploadLocalFilesAndGetMessage(self, args):
    """upload user local files and creates a RayBatch message.

    Upload user local files and point URIs to the local files to the uploaded
    URIs.
    Creates a RayBatch message from parsed arguments.

    Args:
      args: Parsed arguments.

    Returns:
      RayBatch: A RayBatch message.

    Raises:
      AttributeError: Bucket is required to upload local files, but not
      specified.
    """
    kwargs = {}

    if args.args:
      kwargs['args'] = args.args

    dependencies = {}

    # Upload requires a list.
    dependencies['mainPythonFileUri'] = [args.MAIN_PYTHON_FILE]

    if local_file_uploader.HasLocalFiles(dependencies):
      if not args.deps_bucket:
        raise AttributeError('--deps-bucket was not specified.')
      dependencies = local_file_uploader.Upload(args.deps_bucket, dependencies)

    # Move mainPythonFileUri out of the list.
    dependencies['mainPythonFileUri'] = dependencies['mainPythonFileUri'][0]

    # Merge the dict first for compatibility.
    # Old python versions don't support multi unpacking of dictionaries.
    kwargs.update(dependencies)

    return self.dataproc.messages.RayBatch(**kwargs)


def AddArguments(parser):
  """Adds arguments related to RayBatch message."""
  flags.AddMainPythonFile(parser)
  flags.AddArgs(parser)
  # Cloud Storage bucket to upload workload dependencies.
  # It is required until we figure out a place to upload user files.
  flags.AddBucket(parser)

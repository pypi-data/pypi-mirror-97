#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
from abc import ABC, abstractmethod
from typing import Optional


class GraknOptions(ABC):

    def __init__(self):
        self.infer: Optional[bool] = None
        self.trace_inference: Optional[bool] = None
        self.explain: Optional[bool] = None
        self.parallel: Optional[bool] = None
        self.batch_size: Optional[int] = None

    @staticmethod
    def core() -> "GraknOptions":
        return _GraknOptions()

    @staticmethod
    def cluster() -> "GraknClusterOptions":
        return _GraknClusterOptions()

    @abstractmethod
    def is_cluster(self) -> bool:
        pass


class GraknClusterOptions(GraknOptions, ABC):

    def __init__(self):
        super().__init__()
        self.read_any_replica: Optional[bool] = None


class _GraknOptions(GraknOptions):

    def is_cluster(self) -> bool:
        return False


class _GraknClusterOptions(GraknClusterOptions):

    def is_cluster(self) -> bool:
        return True

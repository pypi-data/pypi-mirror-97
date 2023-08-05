# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from aliyunsdkcore.request import RpcRequest
from aliyunsdkdcdn.endpoint import endpoint_data

class SetDcdnConfigOfVersionRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'dcdn', '2018-01-15', 'SetDcdnConfigOfVersion')
		self.set_method('POST')
		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())


	def get_VersionId(self):
		return self.get_query_params().get('VersionId')

	def set_VersionId(self,VersionId):
		self.add_query_param('VersionId',VersionId)

	def get_SecurityToken(self):
		return self.get_query_params().get('SecurityToken')

	def set_SecurityToken(self,SecurityToken):
		self.add_query_param('SecurityToken',SecurityToken)

	def get_FunctionName(self):
		return self.get_query_params().get('FunctionName')

	def set_FunctionName(self,FunctionName):
		self.add_query_param('FunctionName',FunctionName)

	def get_FunctionArgs(self):
		return self.get_query_params().get('FunctionArgs')

	def set_FunctionArgs(self,FunctionArgs):
		self.add_query_param('FunctionArgs',FunctionArgs)

	def get_OwnerAccount(self):
		return self.get_query_params().get('OwnerAccount')

	def set_OwnerAccount(self,OwnerAccount):
		self.add_query_param('OwnerAccount',OwnerAccount)

	def get_OwnerId(self):
		return self.get_query_params().get('OwnerId')

	def set_OwnerId(self,OwnerId):
		self.add_query_param('OwnerId',OwnerId)

	def get_FunctionId(self):
		return self.get_query_params().get('FunctionId')

	def set_FunctionId(self,FunctionId):
		self.add_query_param('FunctionId',FunctionId)

	def get_ConfigId(self):
		return self.get_query_params().get('ConfigId')

	def set_ConfigId(self,ConfigId):
		self.add_query_param('ConfigId',ConfigId)
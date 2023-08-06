from localstack.utils.aws import aws_models
IFJVm=super
IFJVz=None
IFJVW=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  IFJVm(LambdaLayer,self).__init__(arn)
  self.cwd=IFJVz
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.IFJVW.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,IFJVW,env=IFJVz):
  IFJVm(RDSDatabase,self).__init__(IFJVW,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,IFJVW,env=IFJVz):
  IFJVm(RDSCluster,self).__init__(IFJVW,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,IFJVW,env=IFJVz):
  IFJVm(AppSyncAPI,self).__init__(IFJVW,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,IFJVW,env=IFJVz):
  IFJVm(AmplifyApp,self).__init__(IFJVW,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,IFJVW,env=IFJVz):
  IFJVm(ElastiCacheCluster,self).__init__(IFJVW,env=env)
class TransferServer(BaseComponent):
 def __init__(self,IFJVW,env=IFJVz):
  IFJVm(TransferServer,self).__init__(IFJVW,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,IFJVW,env=IFJVz):
  IFJVm(CloudFrontDistribution,self).__init__(IFJVW,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,IFJVW,env=IFJVz):
  IFJVm(CodeCommitRepository,self).__init__(IFJVW,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)

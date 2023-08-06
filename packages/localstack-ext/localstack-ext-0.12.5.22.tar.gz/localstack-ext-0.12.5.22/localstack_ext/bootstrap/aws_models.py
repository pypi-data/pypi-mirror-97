from localstack.utils.aws import aws_models
DREau=super
DREal=None
DREab=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  DREau(LambdaLayer,self).__init__(arn)
  self.cwd=DREal
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.DREab.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,DREab,env=DREal):
  DREau(RDSDatabase,self).__init__(DREab,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,DREab,env=DREal):
  DREau(RDSCluster,self).__init__(DREab,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,DREab,env=DREal):
  DREau(AppSyncAPI,self).__init__(DREab,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,DREab,env=DREal):
  DREau(AmplifyApp,self).__init__(DREab,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,DREab,env=DREal):
  DREau(ElastiCacheCluster,self).__init__(DREab,env=env)
class TransferServer(BaseComponent):
 def __init__(self,DREab,env=DREal):
  DREau(TransferServer,self).__init__(DREab,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,DREab,env=DREal):
  DREau(CloudFrontDistribution,self).__init__(DREab,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,DREab,env=DREal):
  DREau(CodeCommitRepository,self).__init__(DREab,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)

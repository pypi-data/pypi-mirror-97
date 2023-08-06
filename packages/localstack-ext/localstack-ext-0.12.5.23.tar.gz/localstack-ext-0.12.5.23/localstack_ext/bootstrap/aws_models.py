from localstack.utils.aws import aws_models
YfLkb=super
YfLkj=None
YfLkE=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  YfLkb(LambdaLayer,self).__init__(arn)
  self.cwd=YfLkj
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.YfLkE.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,YfLkE,env=YfLkj):
  YfLkb(RDSDatabase,self).__init__(YfLkE,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,YfLkE,env=YfLkj):
  YfLkb(RDSCluster,self).__init__(YfLkE,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,YfLkE,env=YfLkj):
  YfLkb(AppSyncAPI,self).__init__(YfLkE,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,YfLkE,env=YfLkj):
  YfLkb(AmplifyApp,self).__init__(YfLkE,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,YfLkE,env=YfLkj):
  YfLkb(ElastiCacheCluster,self).__init__(YfLkE,env=env)
class TransferServer(BaseComponent):
 def __init__(self,YfLkE,env=YfLkj):
  YfLkb(TransferServer,self).__init__(YfLkE,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,YfLkE,env=YfLkj):
  YfLkb(CloudFrontDistribution,self).__init__(YfLkE,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,YfLkE,env=YfLkj):
  YfLkb(CodeCommitRepository,self).__init__(YfLkE,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)

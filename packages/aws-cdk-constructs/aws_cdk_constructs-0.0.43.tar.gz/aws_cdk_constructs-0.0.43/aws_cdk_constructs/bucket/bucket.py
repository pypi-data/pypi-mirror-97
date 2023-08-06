from aws_cdk import (
    aws_s3 as _s3,
    aws_iam as _iam,
    core,
)
from aws_cdk.core import Tags
import boto3


def check_if_bucket_exist(s3_bucket_name, profile=None):
    aws_session = boto3.Session(profile_name=profile)
    sdk_s3 = aws_session.client("s3")
    bucket_exist = True

    if not s3_bucket_name:
        return False

    try:
        sdk_s3.get_bucket_location(Bucket=s3_bucket_name)
    except:
        bucket_exist = False

    return bucket_exist

class Bucket(core.Construct):
    """ Construct to create an S3 Bucket

    Args:

        id (str): the logical id of the newly created resource
        
        app_name (str): The application name. This will be used to generate the 'ApplicationName' tag for CSI compliancy. The ID of the application. This must be unique for each system, as it will be used to calculate the AWS costs of the system

        environment (str): Specify the environment in which you want to deploy you system. Allowed values: Development, QA, Production, SharedServices 

        environments_parameters (dict): The dictionary containing the references to CSI AWS environments. This will simplify the environment promotions and enable a parametric development of the infrastructures.

        bucket_name (str): The S3 Bucket in which the application S3 are stored
        
        bucket_is_public (str): Wheather or not the S3 bucket should be public

        bucket_is_privately_accessed_from_vpc_over_http_over_http (str): Force the bucket to be private and enable HTTP private accessed from within the VPC. When this parameter is set to True, `bucket_is_public` and `bucket_has_cdn` will be forced to be False
        
        bucket_has_cdn (str): Wheather or not the S3 bucket will be serverd by a Cloudflare CDN
        
        bucket_website_index_document (str): Use this parameter to configure the S3 bucket as Web Hosting. This is the S3 key of the index document of your static site (generally is index.html)
        
        bucket_website_error_document (str): Use this parameter to configure the S3 bucket as Web Hosting. This is the S3 key of the error document of your static site (generally is error.html)

    """
    @property
    def get_s3_bucket(self):
        """Returns the S3 bucket

        Returns:
            aws_s3.Bucket: the S3 bucket
        """
        return self.bucket


    def create_bucket(
        self,
        logic_id,
        bucket_name,
        app_name,
        access_control=None,
        public_read_access=False,
        website_index_document=None,
        website_error_document=None,
        removal_policy=None,
        **kwargs
    ):
        """Create an S3 bucket

        Args:

            logic_id (str): The logical ID of the S3 Bucket
            
            bucket_name (str): The S3 Bucket name

            app_name (str): The application name. This will be used to generate the 'ApplicationName' tag for CSI compliancy. The ID of the application. This must be unique for each system, as it will be used to calculate the AWS costs of the system
            
            access_control (aws_cdk.aws_s3.BucketAccessControl): The S3 Bucket access control policy. For more info see `access_control` in https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_s3/Bucket.html
            
            website_index_document (str): Use this parameter to configure the S3 bucket as Web Hosting. This is the S3 key of the index document of your static site (generally is index.html)
            
            website_error_document (str): Use this parameter to configure the S3 bucket as Web Hosting. This is the S3 key of the error document of your static site (generally is error.html)
            
            removal_policy (aws_cdk.core.RemovalPolicy): The S3 Bucket removal policy. For more info see `removal_policy` in https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_s3/Bucket.html

        Returns:
            aws_s3.Bucket: the S3 bucket
        """
        # Create S3 bucket
        s3_bucket = _s3.Bucket(
            self,
            logic_id,
            bucket_name=bucket_name,
            access_control=access_control,
            public_read_access=public_read_access,
            website_index_document=website_index_document,
            website_error_document=website_error_document,
            removal_policy=removal_policy,
        )

        Tags.of(s3_bucket).add("ApplicationName", app_name,)

        return s3_bucket

    def __init__(
        self,
        scope: core.Construct,
        id: str,
        app_name,
        environment,
        environments_parameters,
        bucket_name,
        bucket_is_public=None,
        bucket_has_cdn=None,
        bucket_website_index_document=None,
        bucket_website_error_document=None,
        bucket_is_privately_accessed_from_vpc_over_http=False,
        **kwargs
    ):
        super().__init__(scope, id, **kwargs)

        # Apply mandatory tags
        Tags.of(self).add("ApplicationName", app_name.lower().strip())
        Tags.of(self).add("Environment", environment)

        # Declare variables
        self.bucket = None

        environment = environment.lower()
        aws_account = environments_parameters["accounts"][environment]
        account_id = aws_account["id"]

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Create conditions
        # bucket_name_was_provided = bucket_name.strip()
        # bucket_already_exist = check_if_bucket_exist(
        #     s3_bucket_name=bucket_name
        # )

        # Check if bucket has to be public
        public_read_access = (
            bucket_is_public
            and isinstance(bucket_is_public, str)
            and bucket_is_public.lower() == "true"
        )

        include_cdn = (
            bucket_has_cdn
            and isinstance(bucket_has_cdn, str)
            and bucket_has_cdn.lower() == "true"
        )

        is_production = environment.lower().strip() == "production"
        is_not_production = not is_production

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Conditionally create resources

        # Only retain production bucket, with public assets
        removal_policy = core.RemovalPolicy.DESTROY
        if is_production and public_read_access:
            removal_policy = core.RemovalPolicy.RETAIN

        # Default access level: PRIVATE
        self.bucket = self.create_bucket(
            logic_id="S3",
            app_name=app_name,
            bucket_name=bucket_name,
            website_index_document=bucket_website_index_document,
            website_error_document=bucket_website_error_document,
            removal_policy=removal_policy,
            access_control=_s3.BucketAccessControl.PRIVATE if not public_read_access else None,
            block_public_access=_s3.BlockPublicAccess.BLOCK_ALL if not public_read_access else None,  # https://docs.aws.amazon.com/AmazonS3/latest/dev/access-control-block-public-access.html
        )

        if bucket_is_privately_accessed_from_vpc_over_http:
            # Force public read to false
            public_read_access=False
            bucket_has_cdn=False

            self.bucket.add_to_resource_policy(
                _iam.PolicyStatement(
                    principals=[_iam.Anyone()],
                    actions=["s3:GetObject"],
                    resources=[
                        "arn:aws:s3:::" + bucket_name,
                        "arn:aws:s3:::" + bucket_name + "/*",
                    ],
                    #conditions={"StringEquals": {"aws:sourceVpce": aws_account["vpc"]}},
                )
            )


        if public_read_access:
            # Grant access to anyone
            self.bucket.grant_public_access()

            self.bucket.add_cors_rule(
                allowed_methods=[
                    _s3.HttpMethods.GET,
                    _s3.HttpMethods.POST,
                    _s3.HttpMethods.PUT,
                    _s3.HttpMethods.DELETE,
                    _s3.HttpMethods.HEAD,
                ],
                allowed_origins=["*"],
                allowed_headers=["*"],
            )

        # Limit access to CDN
        if include_cdn:

            # Cloudflare doc https://support.cloudflare.com/hc/en-us/articles/360037983412-Configuring-an-Amazon-Web-Services-static-site-to-use-Cloudflare
            cloudflare_ips = [
                "2400:cb00::/32",
                "2405:8100::/32",
                "2405:b500::/32",
                "2606:4700::/32",
                "2803:f800::/32",
                "2c0f:f248::/32",
                "2a06:98c0::/29",
                "103.21.244.0/22",
                "103.22.200.0/22",
                "103.31.4.0/22",
                "104.16.0.0/12",
                "108.162.192.0/18",
                "131.0.72.0/22",
                "141.101.64.0/18",
                "162.158.0.0/15",
                "172.64.0.0/13",
                "173.245.48.0/20",
                "188.114.96.0/20",
                "190.93.240.0/20",
                "197.234.240.0/22",
                "198.41.128.0/17",
            ]

            # Only allow access from Cloudflare IPs
            self.bucket.add_to_resource_policy(
                _iam.PolicyStatement(
                    effect=_iam.Effect.DENY,
                    principals=[_iam.Anyone()],
                    actions=["s3:GetObject"],
                    resources=[
                        "arn:aws:s3:::" + bucket_name + "/*",
                    ],
                    conditions={"NotIpAddress": {"aws:SourceIp": cloudflare_ips}},
                )
            )
            self.bucket.add_to_resource_policy(
                _iam.PolicyStatement(
                    effect=_iam.Effect.ALLOW,
                    principals=[_iam.Anyone()],
                    actions=["s3:GetObject"],
                    resources=[
                        "arn:aws:s3:::" + bucket_name + "/*",
                    ],
                    conditions={"IpAddress": {"aws:SourceIp": cloudflare_ips}},
                )
            )

            self.bucket.add_cors_rule(
                allowed_methods=[
                    _s3.HttpMethods.GET,
                    _s3.HttpMethods.POST,
                    _s3.HttpMethods.PUT,
                    _s3.HttpMethods.DELETE,
                    _s3.HttpMethods.HEAD,
                ],
                allowed_origins=["*"],
                allowed_headers=["*"],
            )

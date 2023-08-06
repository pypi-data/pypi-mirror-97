# AWS App Mesh Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

![cdk-constructs: Developer Preview](https://img.shields.io/badge/cdk--constructs-developer--preview-informational.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are in **developer preview** before they
> become stable. We will only make breaking changes to address unforeseen API issues. Therefore,
> these APIs are not subject to [Semantic Versioning](https://semver.org/), and breaking changes
> will be announced in release notes. This means that while you may use them, you may need to
> update your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

AWS App Mesh is a service mesh based on the [Envoy](https://www.envoyproxy.io/) proxy that makes it easy to monitor and control microservices. App Mesh standardizes how your microservices communicate, giving you end-to-end visibility and helping to ensure high-availability for your applications.

App Mesh gives you consistent visibility and network traffic controls for every microservice in an application.

App Mesh supports microservice applications that use service discovery naming for their components. To use App Mesh, you must have an existing application running on AWS Fargate, Amazon ECS, Amazon EKS, Kubernetes on AWS, or Amazon EC2.

For futher information on **AWS AppMesh** visit the [AWS Docs for AppMesh](https://docs.aws.amazon.com/app-mesh/index.html).

## Create the App and Stack

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
app = cdk.App()
stack = cdk.Stack(app, "stack")
```

## Creating the Mesh

A service mesh is a logical boundary for network traffic between the services that reside within it.

After you create your service mesh, you can create virtual services, virtual nodes, virtual routers, and routes to distribute traffic between the applications in your mesh.

The following example creates the `AppMesh` service mesh with the default filter of `DROP_ALL`, see [docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-mesh-egressfilter.html) here for more info on egress filters.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
mesh = Mesh(stack, "AppMesh",
    mesh_name="myAwsmMesh"
)
```

The mesh can also be created with the "ALLOW_ALL" egress filter by overwritting the property.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
mesh = Mesh(stack, "AppMesh",
    mesh_name="myAwsmMesh",
    egress_filter=MeshFilterType.ALLOW_ALL
)
```

## Adding VirtualRouters

The *Mesh* needs *VirtualRouters* as logical units to route requests to *VirtualNodes*.

Virtual routers handle traffic for one or more virtual services within your mesh.
After you create a virtual router, you can create and associate routes to your virtual router that direct incoming requests to different virtual nodes.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
router = mesh.add_virtual_router("router",
    listeners=[appmesh.VirtualRouterListener.http(8080)]
)
```

The router can also be created using the constructor and passing in the mesh instead of calling the `addVirtualRouter()` method for the mesh.
The same pattern applies to all constructs within the appmesh library, for any mesh.addXZY method, a new constuctor can also be used.
This is particularly useful for cross stack resources are required.
Where creating the `mesh` as part of an infrastructure stack and creating the `resources` such as `nodes` is more useful to keep in the application stack.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
mesh = Mesh(stack, "AppMesh",
    mesh_name="myAwsmMesh",
    egress_filter=MeshFilterType.Allow_All
)

router = VirtualRouter(stack, "router",
    mesh=mesh, # notice that mesh is a required property when creating a router with a new statement
    listeners=[appmesh.VirtualRouterListener.http(8081)]
)
```

The *VirtualRouterListener* class provides an easy interface for defining new protocol specific listeners.
The `http()`, `http2()`, `grpc()` and `tcp()` methods are available for use.
They accept a single port parameter, that is used to define what port to match requests on.
The port parameter can be omitted, and it will default to port 8080.

## Adding VirtualService

A virtual service is an abstraction of a real service that is provided by a virtual node directly or indirectly by means of a virtual router. Dependent services call your virtual service by its virtualServiceName, and those requests are routed to the virtual node or virtual router that is specified as the provider for the virtual service.

We recommend that you use the service discovery name of the real service that you're targeting (such as `my-service.default.svc.cluster.local`).

When creating a virtual service:

* If you want the virtual service to spread traffic across multiple virtual nodes, specify a Virtual router.
* If you want the virtual service to reach a virtual node directly, without a virtual router, specify a Virtual node.

Adding a virtual router as the provider:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
appmesh.VirtualService("virtual-service",
    virtual_service_name="my-service.default.svc.cluster.local", # optional
    virtual_service_provider=appmesh.VirtualServiceProvider.virtual_router(router)
)
```

Adding a virtual node as the provider:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
appmesh.VirtualService("virtual-service",
    virtual_service_name="my-service.default.svc.cluster.local", # optional
    virtual_service_provider=appmesh.VirtualServiceProvider.virtual_node(node)
)
```

## Adding a VirtualNode

A `virtual node` acts as a logical pointer to a particular task group, such as an Amazon ECS service or a Kubernetes deployment.

When you create a `virtual node`, any inbound traffic that your `virtual node` expects should be specified as a listener. Any outbound traffic that your `virtual node` expects to reach should be specified as a backend.

The response metadata for your new `virtual node` contains the Amazon Resource Name (ARN) that is associated with the `virtual node`. Set this value (either the full ARN or the truncated resource name) as the APPMESH_VIRTUAL_NODE_NAME environment variable for your task group's Envoy proxy container in your task definition or pod spec. For example, the value could be mesh/default/virtualNode/simpleapp. This is then mapped to the node.id and node.cluster Envoy parameters.

> Note
> If you require your Envoy stats or tracing to use a different name, you can override the node.cluster value that is set by APPMESH_VIRTUAL_NODE_NAME with the APPMESH_VIRTUAL_NODE_CLUSTER environment variable.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
vpc = ec2.Vpc(stack, "vpc")
namespace = servicediscovery.PrivateDnsNamespace(self, "test-namespace",
    vpc=vpc,
    name="domain.local"
)
service = namespace.create_service("Svc")

node = mesh.add_virtual_node("virtual-node",
    service_discovery=appmesh.ServiceDiscovery.cloud_map(
        service=service
    ),
    listeners=[appmesh.VirtualNodeListener.http_node_listener(
        port=8081,
        health_check={
            "healthy_threshold": 3,
            "interval": Duration.seconds(5), # minimum
            "path": "/health-check-path",
            "port": 8080,
            "protocol": Protocol.HTTP,
            "timeout": Duration.seconds(2), # minimum
            "unhealthy_threshold": 2
        }
    )],
    access_log=appmesh.AccessLog.from_file_path("/dev/stdout")
)
```

Create a `VirtualNode` with the constructor and add tags.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
node = VirtualNode(self, "node",
    mesh=mesh,
    service_discovery=appmesh.ServiceDiscovery.cloud_map(
        service=service
    ),
    listeners=[appmesh.VirtualNodeListener.http_node_listener(
        port=8080,
        health_check={
            "healthy_threshold": 3,
            "interval": Duration.seconds(5), # min
            "path": "/ping",
            "port": 8080,
            "protocol": Protocol.HTTP,
            "timeout": Duration.seconds(2), # min
            "unhealthy_threshold": 2
        },
        timeout={
            "idle": cdk.Duration.seconds(5)
        }
    )],
    backends_default_client_policy=appmesh.ClientPolicy.file_trust(
        certificate_chain="/keys/local_cert_chain.pem"
    ),
    access_log=appmesh.AccessLog.from_file_path("/dev/stdout")
)

cdk.Tag.add(node, "Environment", "Dev")
```

Create a `VirtualNode` with the constructor and add backend virtual service.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
node = VirtualNode(self, "node",
    mesh=mesh,
    service_discovery=appmesh.ServiceDiscovery.cloud_map(
        service=service
    ),
    listeners=[appmesh.VirtualNodeListener.http_node_listener(
        port=8080,
        health_check={
            "healthy_threshold": 3,
            "interval": Duration.seconds(5), # min
            "path": "/ping",
            "port": 8080,
            "protocol": Protocol.HTTP,
            "timeout": Duration.seconds(2), # min
            "unhealthy_threshold": 2
        },
        timeout={
            "idle": cdk.Duration.seconds(5)
        }
    )],
    access_log=appmesh.AccessLog.from_file_path("/dev/stdout")
)

virtual_service = appmesh.VirtualService(stack, "service-1",
    service_discovery=appmesh.ServiceDiscovery.dns("service1.domain.local"),
    mesh=mesh,
    client_policy=appmesh.ClientPolicy.file_trust(
        certificate_chain="/keys/local_cert_chain.pem",
        ports=[8080, 8081]
    )
)

node.add_backend(virtual_service)
```

The `listeners` property can be left blank and added later with the `node.addListener()` method. The `healthcheck` and `timeout` properties are optional but if specifying a listener, the `port` must be added.

The `backends` property can be added with `node.addBackend()`. We define a virtual service and add it to the virtual node to allow egress traffic to other node.

The `backendsDefaultClientPolicy` property are added to the node while creating the virtual node. These are virtual node's service backends client policy defaults.

## Adding TLS to a listener

The `tlsCertificate` property can be added to a Virtual Node listener or Virtual Gateway listener to add TLS configuration.
A certificate from AWS Certificate Manager can be incorporated or a customer provided certificate can be specified with a `certificateChain` path file and a `privateKey` file path.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_certificatemanager as certificatemanager

# A Virtual Node with listener TLS from an ACM provided certificate
cert = certificatemanager.Certificate(self, "cert", ...)

node = appmesh.VirtualNode(stack, "node",
    mesh=mesh,
    dns_host_name="node",
    listeners=[appmesh.VirtualNodeListener.grpc(
        port=80,
        tls_certificate=appmesh.TlsCertificate.acm(
            certificate=cert,
            tls_mode=TlsMode.STRICT
        )
    )]
)

# A Virtual Gateway with listener TLS from a customer provided file certificate
gateway = appmesh.VirtualGateway(self, "gateway",
    mesh=mesh,
    listeners=[appmesh.VirtualGatewayListener.grpc(
        port=8080,
        tls_certificate=appmesh.TlsCertificate.file(
            certificate_chain="path/to/certChain",
            private_key="path/to/privateKey",
            tls_mode=TlsMode.STRICT
        )
    )],
    virtual_gateway_name="gateway"
)
```

## Adding a Route

A `route` is associated with a virtual router, and it's used to match requests for a virtual router and distribute traffic accordingly to its associated virtual nodes.

If your `route` matches a request, you can distribute traffic to one or more target virtual nodes with relative weighting.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
router.add_route("route-http",
    route_spec=appmesh.RouteSpec.http(
        weighted_targets=[{
            "virtual_node": node
        }
        ],
        match={
            "prefix_path": "/path-to-app"
        }
    )
)
```

Add a single route with multiple targets and split traffic 50/50

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
router.add_route("route-http",
    route_spec=appmesh.RouteSpec.http(
        weighted_targets=[{
            "virtual_node": node,
            "weight": 50
        }, {
            "virtual_node": node,
            "weight": 50
        }
        ],
        match={
            "prefix_path": "/path-to-app"
        }
    )
)
```

The *RouteSpec* class provides an easy interface for defining new protocol specific route specs.
The `tcp()`, `http()` and `http2()` methods provide the spec necessary to define a protocol specific spec.

For HTTP based routes, the match field can be used to match on a route prefix.
By default, an HTTP based route will match on `/`. All matches must start with a leading `/`.
The timeout field can also be specified for `idle` and `perRequest` timeouts.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
router.add_route("route-http",
    route_spec=appmesh.RouteSpec.grpc(
        weighted_targets=[{
            "virtual_node": node
        }
        ],
        match={
            "service_name": "my-service.default.svc.cluster.local"
        },
        timeout={
            "idle": Duration.seconds(2),
            "per_request": Duration.seconds(1)
        }
    )
)
```

## Adding a Virtual Gateway

A *virtual gateway* allows resources outside your mesh to communicate to resources that are inside your mesh.
The virtual gateway represents an Envoy proxy running in an Amazon ECS task, in a Kubernetes service, or on an Amazon EC2 instance.
Unlike a virtual node, which represents an Envoy running with an application, a virtual gateway represents Envoy deployed by itself.

A virtual gateway is similar to a virtual node in that it has a listener that accepts traffic for a particular port and protocol (HTTP, HTTP2, GRPC).
The traffic that the virtual gateway receives, is directed to other services in your mesh,
using rules defined in gateway routes which can be added to your virtual gateway.

Create a virtual gateway with the constructor:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
certificate_authority_arn = "arn:aws:acm-pca:us-east-1:123456789012:certificate-authority/12345678-1234-1234-1234-123456789012"

gateway = appmesh.VirtualGateway(stack, "gateway",
    mesh=mesh,
    listeners=[appmesh.VirtualGatewayListener.http(
        port=443,
        health_check={
            "interval": cdk.Duration.seconds(10)
        }
    )],
    backends_default_client_policy=appmesh.ClientPolicy.acm_trust(
        certificate_authorities=[acmpca.CertificateAuthority.from_certificate_authority_arn(stack, "certificate", certificate_authority_arn)],
        ports=[8080, 8081]
    ),
    access_log=appmesh.AccessLog.from_file_path("/dev/stdout"),
    virtual_gateway_name="virtualGateway"
)
```

Add a virtual gateway directly to the mesh:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
gateway = mesh.add_virtual_gateway("gateway",
    access_log=appmesh.AccessLog.from_file_path("/dev/stdout"),
    virtual_gateway_name="virtualGateway",
    listeners=[appmesh.VirtualGatewayListener.http(
        port=443,
        health_check={
            "interval": cdk.Duration.seconds(10)
        }
    )]
)
```

The listeners field can be omitted which will default to an HTTP Listener on port 8080.
A gateway route can be added using the `gateway.addGatewayRoute()` method.

The `backendsDefaultClientPolicy` property are added to the node while creating the virtual gateway. These are virtual gateway's service backends client policy defaults.

## Adding a Gateway Route

A *gateway route* is attached to a virtual gateway and routes traffic to an existing virtual service.
If a route matches a request, it can distribute traffic to a target virtual service.

For HTTP based routes, the match field can be used to match on a route prefix.
By default, an HTTP based route will match on `/`. All matches must start with a leading `/`.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
gateway.add_gateway_route("gateway-route-http",
    route_spec=appmesh.GatewayRouteSpec.http(
        route_target=virtual_service,
        match={
            "prefix_match": "/"
        }
    )
)
```

For GRPC based routes, the match field can be used to match on service names.
You cannot omit the field, and must specify a match for these routes.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
gateway.add_gateway_route("gateway-route-grpc",
    route_spec=appmesh.GatewayRouteSpec.grpc(
        route_target=virtual_service,
        match={
            "service_name": "my-service.default.svc.cluster.local"
        }
    )
)
```

## Importing Resources

Each mesh resource comes with two static methods for importing a reference to an existing App Mesh resource.
These imported resources can be used as references for other resources in your mesh.
There are two static methods, `from<Resource>Arn` and `from<Resource>Attributes` where the `<Resource>` is replaced with the resource name.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
arn = "arn:aws:appmesh:us-east-1:123456789012:mesh/testMesh/virtualNode/testNode"
appmesh.VirtualNode.from_virtual_node_arn(stack, "importedVirtualNode", arn)
```

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
appmesh.VirtualNode.from_virtual_node_attributes(stack, "imported-virtual-node",
    mesh=appmesh.Mesh.from_mesh_name(stack, "Mesh", "testMesh"),
    virtual_node_name=virtual_node_name
)
```

To import a mesh, there are two static methods, `fromMeshArn` and `fromMeshName`.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
arn = "arn:aws:appmesh:us-east-1:123456789012:mesh/testMesh"
appmesh.Mesh.from_mesh_arn(stack, "imported-mesh", arn)
```

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
appmesh.Mesh.from_mesh_name(stack, "imported-mesh", "abc")
```

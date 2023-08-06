## StackResourceRenamer

#### A CDK aspect, StackResourceRenamer renames CDK stack name and stack's subordinate resources' custom physical names, so that a CDK stack can be used to create multiple stacks in same AWS environment without confliction.

### Sample

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
app = core.App()

stack = core.Stack(app, "my-stack")

alias = stack.node.try_get_context("alias")
if alias !== undefined:
    # if alias is defined, rename stack and resources' custom names
    # with the "rename" function/method.
    StackResourceRenamer.rename(stack,
        rename=(origName, _)=>{
                        return origName+'-'+alias;
                    }
    )

# resources in stack
bucket = s3.Bucket(stack, "bucket",
    bucket_name="my-bucket"
)
```

To create multiple stacks:

`cdk -c alias=a1 deploy  `
will create a stack: my-stack-a1 with my-bucket-a1.

To create more stacks: my-stack-a2 with my-bucket-a2, my-stack-a3 with my-bucket-a3:

`cdk -c alias=a2 deploy`

`cdk -c alias=a3 deploy`

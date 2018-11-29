# flexio-flow

### Version Flow

 ```       
master    0.1.0* -- 0.1.1* -------------------- 0.2.0* ------------
           |   \      /  |                       /
hotfix    |  0.1.1-dev  |                      /    
           |             |                     /
release   |             |                  0.2.0
           |             |                  /    \
develop 0.2.0-dev ----------------------  0.3.0-dev ----------
           \     \                 /                      /
feature1   \       --------------                       /    
             \                                          /      
feature2        --------------------------------------
```


### Specification `flexio-flow.yml`
```yaml
version: 0.0.0
level: stable|dev
scheme: maven|package|composer|docker
```

### Main orders
```bash
flexio-flow init
flexio-flow hotfix start
flexio-flow hotfix finish
flexio-flow release start
flexio-flow release plan
flexio-flow release finish
```

# flexio-flow

 - python >= 3.7
 - python-venv >= 3.7
 
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

### Dev environment
#### Virtual environment initialisation 
```bash
bash ./venv.sh
```
#### Activate virtual environment
```bash
source $PWD/venv/bin/activate
```
#### Deactivate virtual environment
```bash
deactivate
```

#### Update pip requirements
`with virtual environement activated`
```bash
pip freeze > requirements.txt
````
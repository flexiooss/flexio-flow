l![](git pull)# flexio-flow

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

### Installation
With Ansible playbook : https://github.com/flexiooss/flexio-flow-playbook

### Specification `flexio-flow.yml`
```yaml
version: [\d].[\d].[\d]
level: stable|dev
schemes: maven|package|composer|docker
topics: [\d][]
```

### Main orders
```bash
flexio-flow -h

flexio-flow core config
flexio-flow init
flexio-flow version

flexio-flow commit

flexio-flow hotfix start
flexio-flow hotfix finish

flexio-flow feature start
flexio-flow feature finish

flexio-flow release precheck
flexio-flow release start
flexio-flow release finish

flexio-flow commit

flexio-flow issue read
flexio-flow topics read

flexio-flow scheme update

flexio-flow poom ci full-repository-json
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
python3 -m pip freeze > requirements.txt
````

#### Update pip dependencies
`with virtual environement activated`
```bash
python3 -m pip install -r requirements.txt

````

# recommendation-engine

```bash
cd /tmp/
wget https://www.python.org/ftp/python/3.11.5/Python-3.11.5.tgz
tar -xzvf Python-3.11.5.tgz
cd Python-3.11.5/
apt update
apt install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev
./configure --enable-optimizations
make -j `nproc`
make altinstall
# ln -s /usr/local/bin/python3.11 /usr/local/bin/python
cd /com.docker.devenvironments.code
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade -r requirements.txt
```

# References

<https://towardsdatascience.com/recommender-systems-from-learned-embeddings-f1d12288f278>

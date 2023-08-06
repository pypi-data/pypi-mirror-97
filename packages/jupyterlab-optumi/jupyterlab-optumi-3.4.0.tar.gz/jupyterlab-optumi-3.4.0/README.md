# **Welcome to Optumi 👋**

### Description

Optumi's JupyterLab extension provisions and manages ML environments in the cloud. Data scientists can seamlessly offload local notebooks as interactive sessions or batch jobs while software automatically cleans up infrastructure when no longer needed and makes it easy to keep track of spending.

Our goal is to help you spend more time developing models and less time on infrastructure.

### Installation

Prerequisites:

- Python 3.6 or later
- JupyterLab 3

Install from PyPI:

```pip install jupyterlab-optumi```

*Note: If you are running JupyterLab from an anaconda environment, you'll need to run the install command with that environment activated. You can do this by launching JupyterLab, selecting File -> New -> Terminal and running the install command there. If you do this, you will need to shut down and restart Jupyterlab before using the extension.*

*Note: If you already have the extension installed outside of an anaconda environment and want to reinstall it inside of an anaconda environment, you will need to add the* ```-U``` *flag to the pip install command.*

*Note: Safari browser is not supported.*

Test the install by running
```jupyter lab extension list``` and ```jupyter server extension list```. You should see **jupyterlab_optumi** in both outputs.

If you do not see **jupyterlab_optumi** in both outputs, run ```jupyter server extension enable jupyterlab_optumi --user``` and test the install again.

Start JupyterLab and you'll see  <img src="https://drive.google.com/uc?export=view&id=1Cf7_RCL8LLxFFp9ByfZB9-5-SRPghMNB" width="20" height="20" style="vertical-align:middle;"> in the left side bar.

### Questions

If you have any questions, please reach out to the Optumi team. You can contact us by emailing cs@optumi.com or through our website www.optumi.com.


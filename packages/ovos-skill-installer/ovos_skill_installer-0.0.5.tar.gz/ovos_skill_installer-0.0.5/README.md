# OVOS skill installer

Skills can be installed from github branches or releases, from .zip or .tar.gz urls

This tool is meant to be used internally by [ovos_skills_manager](https://github.com/OpenVoiceOS/ovos_skill_manager), as an end user your probably should be using that and not this repository directly. 

## Usage

![](./github_branches.png)


```python
from ovos_skill_installer import install_skill

folder = "extract_here"

# using github branches

url = "https://github.com/MycroftAI/skill-playback-control/archive/20.02.zip"
updated = install_skill(url, folder, "skill-playback.zip")
assert updated == True

# should remove files from above
url = "https://github.com/MycroftAI/skill-playback-control/archive/20.08.zip"
updated = install_skill(url, folder, "skill-playback.zip")
assert updated == True

updated = install_skill(url, folder, "skill-playback.zip")
assert updated == False
```
![](./github_releases.png)

```python
# Using github releases

url = "https://github.com/JarbasSkills/skill-wolfie/archive/v0.1.tar.gz"
updated = install_skill(url, folder, "skill-wolfie.tar.gz")
assert updated == True

# should remove files from above
url = "https://github.com/JarbasSkills/skill-wolfie/archive/v0.1UPDATE_TEST.tar.gz"
updated = install_skill(url, folder, "skill-wolfie.tar.gz")
assert updated == True

updated = install_skill(url, folder, "skill-wolfie.tar.gz")
assert updated == False
```


## Installation

```bash
pip install ovos_skill_installer
```

## Credits

The only reason this is a standalone package is to give proper attribution to [MatthewScholefield](https://github.com/MatthewScholefield), this work is adapted from his work on [petact](https://github.com/matthewscholefield/petact), thanks Matthew!

<h1 align="center">
    </br>
    SamCart Video Collector
</h1>

<h4 align="center">Python script that gathers videos from SamCart courses and downloads them for offline viewing.</h4>

<p align="center">
    <a href="https://github.com/zico-io/SamCartVideoCollector/commits/master">
    <img src="https://img.shields.io/github/last-commit/zico-io/SamCartVideoCollector.svg?style=flat-square&logo=github&logoColor=white"
         alt="GitHub last commit">
    <a href="https://github.com/zico-io/SamCartVideoCollector/issues">
    <img src="https://img.shields.io/github/issues-raw/zico-io/SamCartVideoCollector.svg?style=flat-square&logo=github&logoColor=white"
         alt="GitHub issues">
    <a href="https://github.com/zico-io/SamCartVideoCollector/pulls">
    <img src="https://img.shields.io/github/issues-pr-raw/zico-io/SamCartVideoCollector.svg?style=flat-square&logo=github&logoColor=white"
         alt="GitHub pull requests">
    <br>
    <a href="https://github.com/zico-io/SamCartVideoCollector/blobl/master/LICENSE">
    <img src="https://img.shields.io/apm/l/atomic-design-ui.svg?style=flat-square&logo=github&logoColor=white"
        alt="Github License">
    <a href="https://GitHub.com/zico-io/SamCartVideoCollector/releases/">
    <img src="https://img.shields.io/github/release/zico-io/SamCartVideoCollector.svg"
        alt="Github Release">
    <a href="https://GitHub.com/zico-io/SamCartVideoCollector/commit/">
    <img src="https://badgen.net/github/commits/zico-io/SamCartVideoCollector"
        alt="Github Commits">
    <a href="https://GitHub.com/zico-io/SamCartVideoCollector/commit/">
    <img src="https://badgen.net/github/last-commit/zico-io/SamCartVideoCollector"
        alt="Github Commits">
</p>
<p align="center">
    <a href="#about">About</a> •
    <a href="#getting-started">Getting Started</a> •
    <a href="#usage">Usage</a> •
    <a href="#features">Features</a> •
    <a href="#support">Support</a>
</p>

---
## About
<table>
<tr>
<td>
<br>

Allows the user to download video content from **SamCart** courses they have access to. Intended for archival purposes.
<br>***NOTE:*** **You MUST have access to the course you're attempting to archive, this does not grant the user any special access.**

<p align="right">
<sub>(Preview)</sub>
</p>

</td>
</tr>
</table>

## Getting Started

### Prerequisites
Necessary software and how to install them
#### BeautifulSoup4
```
pip install beautifulsoup4
```
#### Selenium
In order to detect the lessons in the course we must be able to run JavaScript, which BeautifulSoup4 does not allow us to do. For this, we use Selenium as a webdriver that performs the top-level navigation through the course pages.
```
pip install selenium
```
#### Selenium Wire
Selenium by default doesn't come with the ability to capture HTTP requests, which is how we obtain the link to the video file. For this functionality we must use Selenium Wire
```
pip install selenium-wire
```
#### Webdriver Manager
While not necessary, Webdriver Manager allows us to easily install and maintain the binary drivers of our browser.
```
pip install webdriver-manager
```
#### wget
We use wget in order to download the video files from the CDN.
```
pip install wget
```

### Installation
Steps required to get a running development env.

1. **Clone the Repository**
    ```
    git clone https://github.com/zico-io/SamCartVideoCollector
    ```
2. **Install Prerequisites**
    ```
    pip install -r requirements.txt
    ```
    Alternatively you can install them manually using the commands [above](#prerequisites).

3. **Populate Config File**
    <br>Included with the repo is an [example config file](data/config_example.json). Simply make a copy of this file, populate it with the relevant information and rename the file to **config.json**.
## Usage
Once **config.json** has been configured, simply run the program using `python main.py` and follow the terminal prompts.

## Support
- Email: **dev@zico.xyz**

## License
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)
- Copyright © [zico-io](https://zico.xyz "Zico Directory Database").
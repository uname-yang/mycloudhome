# WD My Cloud Home CLI

mycloudhome is a cli tool to manage file on the `West Digital` storage device: `My Cloud Home`. You can check the files on your device in the cli way. Also you can upload or download the file in your command line anywhere without using the WD Client or Web Brower.

Learn more about MY CLOUD HOME from: <https://www.mycloud.com/#/>

## Install

```bash
pip3 install mycloudhome
```

## Usage Examples

Command-line scares you off? No, mycloudhome is really easy to use!!

1. fisrt, we need do a login action. And it will fetch your token and config from `mycloud.com`.

```bash
mycloudhome login --username xxx --password xxx
```

2. get your devices info by:

```bash
mycloudhome devices
```

3. list the files and dirs under the path:

```bash
mycloudhome ls --wduri 'wd://Buckets/install/'
```

>The path on device aways start with 'wd://', and the root of your device is 'wd://'

4. move one file from one location to another:

```bash
mycloudhome mv --src wd://temp/readme.md --dst wd://temp/ttt
```

5. delete file:

```bash
mycloudhome rm --wduri wd://temp/readme_1.md
```

6. create a new WD dir:

```bash
mycloudhome mkdir --wduri wd://temp/cache
```

7. upload the file from local file system to My Cloud Home:

```bash
mycloudhome upload --src 20200518.xlsx --wduri wd://excels
```

8. download file from My Cloud Home to local file system:

```bash
mycloudhome download --wduri 'wd://Buckets/install/v2ray-linux-arm64.zip' --localpath .
```

---

- <https://home.mycloud.com/>
- <https://pypi.org/project/mycloudhome>
- <https://home.mycloud.com/>
